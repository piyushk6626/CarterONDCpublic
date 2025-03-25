"""
Webhook handler for the Cart-ONDC application.

This module provides the API endpoints for handling WhatsApp webhook requests,
including message processing, store registration workflows, and inventory creation.
"""

from flask import Flask, request, jsonify, Blueprint
import time

from cart_ondc.core.firebase import firebase_client
from cart_ondc.services.whatsapp_service import whatsapp_service
from cart_ondc.services.messaging import wait_for_reply, conversation_manager
from cart_ondc.store_types.store_type import store_type_manager
from cart_ondc.registration.registration_factory import RegistrationFactory
from cart_ondc.core.database import db_manager
from cart_ondc.inventory_creation.ICconversation_handler import ask_question
from cart_ondc.inventory_creation.ICdatabase_opration import add_product
from openai import OpenAI
import os
from dotenv import load_dotenv
from pydantic import BaseModel

# Load environment variables
load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")
client = OpenAI(api_key=api_key)

# Create a Blueprint for the webhook routes
webhook_bp = Blueprint('webhook', __name__)

@webhook_bp.route('/', defaults={'path': ''}, methods=['GET'])
@webhook_bp.route('/<path:path>', methods=['GET'])
def handle_verification(path):
    """
    Handle verification requests from the WhatsApp Business API.
    
    Args:
        path (str): The path of the request
        
    Returns:
        str: The challenge string if verification is successful
    """
    # Handle the WhatsApp webhook verification
    verify_token = request.args.get("hub.verify_token")
    challenge = request.args.get("hub.challenge")
    
    # Check if this is a verification request
    if verify_token == "your_verify_token":  # Replace with your verify token
        return challenge
    
    return "Verification failed", 403


@webhook_bp.route('/', defaults={'path': ''}, methods=['POST'])
@webhook_bp.route('/<path:path>', methods=['POST'])
def handle_webhook(path):
    """
    Handle incoming webhook requests from the WhatsApp Business API.
    
    This function processes incoming messages, manages store registration,
    inventory creation, and handles other WhatsApp interactions.
    
    Args:
        path (str): The path of the request
        
    Returns:
        dict: A JSON response indicating success
    """
    print("-------------- New Request POST --------------")
    data = request.json
    
    try:
        # Extract the phone number from the webhook data
        contact_wa_id = data.get('entry', [])[0].get('changes', [])[0].get('value', {}).get('messages', [])[0].get('from', None)
        
        if contact_wa_id is None:
            raise ValueError("Could not read phone number")
        
        # Store the message in Firebase
        firebase_client.add_whatsapp_message(data)
        
        # Check if the user is verified
        verified = db_manager.is_verified(contact_wa_id)
        
        # Handle new user registration
        if not verified:
            # Start the registration process if not already started
            if not conversation_manager.get_conversation_state(contact_wa_id):
                # Send the initial store type selection message
                whatsapp_service.send_message(store_type_manager.select_store_type(), contact_wa_id)
                conversation_manager.start_conversation(contact_wa_id)
                
                # Wait for the user's store type selection
                print(f"Waiting for a reply from {contact_wa_id}...")
                time.sleep(2)  # Give some time for the message to be delivered
                store_type = wait_for_reply(contact_wa_id)
                
                if store_type:
                    # Create the appropriate registration handler
                    try:
                        registration = RegistrationFactory.create_registration(store_type, contact_wa_id)
                        # Start the registration process
                        result = registration.register()
                        
                        if result:
                            whatsapp_service.send_message(
                                "Thank you for completing the registration! Your information has been submitted for verification.", 
                                contact_wa_id
                            )
                        else:
                            # Registration was interrupted or failed
                            whatsapp_service.send_message(
                                "Your registration is incomplete. Please continue when you're ready.", 
                                contact_wa_id
                            )
                    except ValueError as e:
                        # Invalid store type
                        whatsapp_service.send_message(
                            f"Sorry, {store_type} is not a valid store type. Please try again.", 
                            contact_wa_id
                        )
                        # Reset conversation state
                        conversation_manager.update_conversation(contact_wa_id, state='initial', progress=0)
            else:
                # Continue an existing registration process
                state = conversation_manager.get_conversation_state(contact_wa_id)
                if state.get('state') != 'completed':
                    # Get the store type from the conversation state
                    store_type = state.get('data', {}).get('store_type')
                    if store_type:
                        # Continue registration
                        registration = RegistrationFactory.create_registration(store_type, contact_wa_id)
                        result = registration.register()
                        
                        if result:
                            whatsapp_service.send_message(
                                "Thank you for completing the registration! Your information has been submitted for verification.", 
                                contact_wa_id
                            )
        else:
            # User is already verified, handle regular interactions
            # Get the message content
            message_text = data.get('entry', [])[0].get('changes', [])[0].get('value', {}).get('messages', [])[0].get('text', {}).get('body', '').lower()
            
            # Check if this is an inventory creation request
            if message_text.startswith('add product') or message_text.startswith('create product'):
                # Start inventory creation flow
                whatsapp_service.send_message(
                    "Let's create a new product for your inventory. I'll ask you some questions to get started.",
                    contact_wa_id
                )
                
                # Define the Pydantic model for product data
                class ProductData(BaseModel):
                    has_answer: bool
                    product_name: str
                    
                # Ask for product name
                product_name_response = ask_question(
                    client=client,
                    question="What is the name of your product?",
                    response_format_class=ProductData,
                    prompt="Extract the product name from the user's response.",
                    bool_attribute="has_answer",
                    max_attempts=3
                )
                
                if product_name_response and product_name_response.has_answer:
                    # More product information can be collected here
                    # For simplicity, we'll just create a basic product
                    
                    # Create product data
                    product_data = {
                        "id": f"prod_{int(time.time())}",
                        "name": product_name_response.product_name,
                        "seller_id": contact_wa_id,
                        "created_at": time.time()
                    }
                    
                    # Add product to database
                    success = add_product(product_data)
                    
                    if success:
                        whatsapp_service.send_message(
                            f"Your product '{product_name_response.product_name}' has been added to your inventory!",
                            contact_wa_id
                        )
                    else:
                        whatsapp_service.send_message(
                            "Sorry, there was an error adding your product. Please try again later.",
                            contact_wa_id
                        )
                else:
                    whatsapp_service.send_message(
                        "I couldn't get the product name. Let's try again later.",
                        contact_wa_id
                    )
            else:
                # Default response for verified users
                whatsapp_service.send_message(
                    "Welcome back! How can I assist you today? You can say 'add product' to create a new inventory item.",
                    contact_wa_id
                )
    
    except Exception as e:
        print(f"Error processing webhook: {e}")
        # Don't send an error message to the user to avoid confusion
    
    # Always return a 200 response to acknowledge receipt of the webhook
    return jsonify({"status": "success"})

# Function to register the blueprint with the Flask app
def register_webhook(app):
    """
    Register the webhook blueprint with the Flask app.
    
    Args:
        app (Flask): The Flask app
    """
    app.register_blueprint(webhook_bp, url_prefix='/webhook') 