"""
Firebase operations for the Cart-ONDC application.

This module handles all interactions with Firebase including initialization,
data storage, retrieval, and authentication.
"""

import firebase_admin
from firebase_admin import credentials, firestore
import datetime
import os
import json

class FirebaseClient:
    """Manages Firebase Firestore operations for the application."""
    
    _instance = None
    
    def __new__(cls):
        """Implement singleton pattern for Firebase client."""
        if cls._instance is None:
            cls._instance = super(FirebaseClient, cls).__new__(cls)
            cls._instance._initialized = False
        return cls._instance
    
    def __init__(self):
        """Initialize Firebase client if not already initialized."""
        if not self._initialized:
            self._initialize_firebase()
            self._db = firestore.client()
            self._initialized = True
    
    def _initialize_firebase(self):
        """Initialize Firebase Admin SDK if not already initialized."""
        if not firebase_admin._apps:
            try:
                cred = credentials.Certificate("auth.json")
                firebase_admin.initialize_app(cred)
            except Exception as e:
                print(f"Firebase initialization error: {e}")
                raise
    
    def add_whatsapp_message(self, data):
        """
        Add a WhatsApp message document to the Firestore 'WhatsAppMessages' collection.
        
        Args:
            data (dict): The message data from WhatsApp webhook
            
        Returns:
            str: Message ID of the stored message
            
        Raises:
            Exception: If there's an error adding the message
        """
        try:
            # Extract message details
            messaging_product = data.get('entry', [])[0].get('changes', [])[0].get('value', {}).get('messaging_product', None)
            phone_number_id = data.get('entry', [])[0].get('changes', [])[0].get('value', {}).get('metadata', {}).get('phone_number_id', None)
            display_phone_number = data.get('entry', [])[0].get('changes', [])[0].get('value', {}).get('metadata', {}).get('display_phone_number', None)
            contact_wa_id = data.get('entry', [])[0].get('changes', [])[0].get('value', {}).get('contacts', [])[0].get('wa_id', None)
            contact_name = data.get('entry', [])[0].get('changes', [])[0].get('value', {}).get('contacts', [])[0].get('profile', {}).get('name', None)
            message_id = data.get('entry', [])[0].get('changes', [])[0].get('value', {}).get('messages', [])[0].get('id', None)
            timestamp = data.get('entry', [])[0].get('changes', [])[0].get('value', {}).get('messages', [])[0].get('timestamp', None)
            text_body = data.get('entry', [])[0].get('changes', [])[0].get('value', {}).get('messages', [])[0].get('text', {}).get('body', None)
            
            # Prepare Firestore document
            doc = {
                "messaging_product": messaging_product,
                "phone_number_id": phone_number_id,
                "display_phone_number": display_phone_number,
                "contact_wa_id": contact_wa_id,
                "contact_name": contact_name,
                "message_id": message_id,
                "timestamp": timestamp,
                "text_body": text_body,
                "raw_data": data  # Store the full JSON object for reference
            }
            
            # Add the document to the Firestore collection
            collection = self._db.collection("WhatsAppMessages")
            collection.document(message_id).set(doc)
            
            print(f"Message from {contact_wa_id} added successfully with ID: {message_id}")
            return message_id
            
        except Exception as e:
            print(f"An error occurred while adding the WhatsApp message: {e}")
            raise
    
    def get_latest_message(self, phone_number):
        """
        Retrieve the latest message from a specific phone number.
        
        Args:
            phone_number (str): The WhatsApp phone number to get the latest message from
            
        Returns:
            dict: The latest message data or None if no message is found
            
        Raises:
            Exception: If there's an error retrieving the message
        """
        try:
            # Query the Firestore collection to get the latest message from the specified phone number
            collection = self._db.collection("WhatsAppMessages")
            query = (
                collection
                .where("contact_wa_id", "==", phone_number)  # Filter messages from the given phone number
                .order_by("timestamp", direction=firestore.Query.DESCENDING)  # Sort by timestamp (latest first)
                .limit(1)  # Limit the query to one document
            )
            
            # Execute the query
            results = query.stream()
            
            # Iterate through the results
            for result in results:
                message_data = result.to_dict()  # Convert Firestore document to a dictionary
                return message_data
            
            # If no message is found
            print(f"No messages found for the phone number: {phone_number}")
            return None
            
        except Exception as e:
            print(f"An error occurred while retrieving the message: {e}")
            return None

# Singleton instance that can be imported
firebase_client = FirebaseClient() 