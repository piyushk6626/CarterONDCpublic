"""
Webhook handler for the Cart-ONDC application.

This module provides the API endpoints for handling WhatsApp webhook requests,
including message processing and store registration workflows.
"""

from flask import Flask, request, jsonify, Blueprint
import time

from cart_ondc.core.firebase import firebase_client
from cart_ondc.services.whatsapp_service import whatsapp_service
from cart_ondc.services.messaging import wait_for_reply, conversation_manager
from cart_ondc.store_types.store_type import store_type_manager
from cart_ondc.registration.registration_factory import RegistrationFactory
from cart_ondc.core.database import db_manager

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
    and handles other WhatsApp interactions.
    
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
            # TODO: Implement logic for handling interactions with verified users
            whatsapp_service.send_message(
                "Welcome back! How can I assist you today?", 
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