"""
WhatsApp messaging services for the Cart-ONDC application.

This module handles sending and receiving WhatsApp messages, including text, audio, 
images, and documents through the WhatsApp Business API.
"""

import requests
import json
import os
from dotenv import load_dotenv
from cart_ondc.core.firebase import firebase_client
from cart_ondc.services.download_service import download_media

# Load environment variables from .env file
load_dotenv()

class WhatsAppService:
    """Service for interacting with WhatsApp Business API."""
    
    def __init__(self):
        """Initialize the WhatsApp service with the required credentials."""
        self.phone_id = os.getenv("PHONE_ID")
        self.access_token = os.getenv("ACCESS_TOKEN")
        self.api_version = "v21.0"  # WhatsApp API version
        self.base_url = f"https://graph.facebook.com/{self.api_version}/{self.phone_id}/messages"
    
    def send_message(self, message, phone_number):
        """
        Send a text message to a WhatsApp phone number.
        
        Args:
            message (str): The message to send
            phone_number (str): The recipient's phone number
            
        Returns:
            bool: True if the message was sent successfully
        """
        # Headers for the request
        headers = {
            "Authorization": f"Bearer {self.access_token}",
            "Content-Type": "application/json"
        }

        # Payload (Message data)
        data = {
            "messaging_product": "whatsapp",
            "to": phone_number,
            "type": "text",
            "text": {
                "body": message
            }
        }

        # Send the POST request to the WhatsApp API
        response = requests.post(self.base_url, headers=headers, data=json.dumps(data))

        # Check if the request was successful
        if response.status_code == 200:
            print(f"Message sent successfully: {message}")
            return True
        else:
            print(f"Failed to send message. Status Code: {response.status_code}, Response: {response.text}")
            return False
    
    def _get_mime_type_from_message(self, message_data):
        """
        Extract MIME type from a message.
        
        Args:
            message_data (dict): The message data
            
        Returns:
            str: MIME type or None if not found
        """
        try:
            # Try to get audio MIME type
            mime_type = (
                message_data.get('raw_data', {})
                .get('entry', [])[0]
                .get('changes', [])[0]
                .get('value', {})
                .get('messages', [])[0]
                .get('audio', {})
                .get('mime_type', None)
            )

            # Try to get image MIME type if audio MIME type not found
            if mime_type is None:
                mime_type = (
                message_data.get('raw_data', {})
                .get('entry', [])[0]
                .get('changes', [])[0]
                .get('value', {})
                .get('messages', [])[0]
                .get('image', {})
                .get('mime_type', None)
             )
                
            # Try to get document MIME type if image MIME type not found
            if mime_type is None:
                mime_type = (
                message_data.get('raw_data', {})
                .get('entry', [])[0]
                .get('changes', [])[0]
                .get('value', {})
                .get('messages', [])[0]
                .get('document', {})
                .get('mime_type', None)
             )

            return mime_type
        except Exception as e:
            print(f"An error occurred while extracting the MIME type: {e}")
            return None
    
    def _get_audio_id(self, message_data):
        """
        Extract audio ID from a message.
        
        Args:
            message_data (dict): The message data
            
        Returns:
            str: Audio ID or None if not found
        """
        try:
            # Extract the audio id field
            audio_id = (
                message_data.get('raw_data', {})
                .get('entry', [])[0]
                .get('changes', [])[0]
                .get('value', {})
                .get('messages', [])[0]
                .get('audio', {})
                .get('id', None)
            )
            return audio_id
        except Exception as e:
            print(f"An error occurred while extracting the audio id: {e}")
            return None
    
    def _get_image_id(self, message_data):
        """
        Extract image ID from a message.
        
        Args:
            message_data (dict): The message data
            
        Returns:
            str: Image ID or None if not found
        """
        try:
            # Extract the image id field
            image_id = (
                message_data.get('raw_data', {})
                .get('entry', [])[0]
                .get('changes', [])[0]
                .get('value', {})
                .get('messages', [])[0]
                .get('image', {})
                .get('id', None)
            )
            
            return image_id
        
        except Exception as e:
            print(f"An error occurred while extracting the image id: {e}")
            return None
    
    def _get_document_id(self, message_data):
        """
        Extract document ID from a message.
        
        Args:
            message_data (dict): The message data
            
        Returns:
            str: Document ID or None if not found
        """
        try:
            # Extract the document id field
            doc_id = (
                message_data.get('raw_data', {})
                .get('entry', [])[0]
                .get('changes', [])[0]
                .get('value', {})
                .get('messages', [])[0]
                .get('document', {})
                .get('id', None)
            )
            
            return doc_id
        
        except Exception as e:
            print(f"An error occurred while extracting the document id: {e}")
            return None
    
    def receive_message(self, phone_number):
        """
        Receive and process a text message from a WhatsApp phone number.
        
        Args:
            phone_number (str): The sender's phone number
            
        Returns:
            str: The received text message or None if not found
        """
        data = firebase_client.get_latest_message(phone_number)
        mime_type = self._get_mime_type_from_message(data)
        
        if mime_type is None:
            text_body = data.get('text_body', None)
            print(f"Reply was {text_body}")
            return text_body
        else:
            self.send_message("Expecting Text Input", phone_number)
            return None
    
    def receive_audio(self, phone_number):
        """
        Receive and process an audio message from a WhatsApp phone number.
        
        Args:
            phone_number (str): The sender's phone number
            
        Returns:
            str: Path to the downloaded audio file or None if not found
        """
        data = firebase_client.get_latest_message(phone_number)
        mime_type = self._get_mime_type_from_message(data)
        
        if mime_type == "audio/ogg; codecs=opus":
            timestamp = (
                data.get('raw_data', {})
                .get('entry', [])[0]
                .get('changes', [])[0]
                .get('value', {})
                .get('messages', [])[0]
                .get('timestamp', None)
            )
            file_id = self._get_audio_id(data)
            file_path = download_media(file_id, "audio/ogg", timestamp, phone_number)
            return file_path
        else:
            self.send_message("Expecting Audio Input", phone_number)
            return None
    
    def receive_image(self, phone_number):
        """
        Receive and process an image message from a WhatsApp phone number.
        
        Args:
            phone_number (str): The sender's phone number
            
        Returns:
            str: Path to the downloaded image file or None if not found
        """
        data = firebase_client.get_latest_message(phone_number)
        mime_type = self._get_mime_type_from_message(data)
        
        if mime_type and mime_type.split('/')[0] == "image":
            timestamp = (
                data.get('raw_data', {})
                .get('entry', [])[0]
                .get('changes', [])[0]
                .get('value', {})
                .get('messages', [])[0]
                .get('timestamp', None)
            )
            file_id = self._get_image_id(data)
            file_path = download_media(file_id, mime_type, timestamp, phone_number)
            return file_path
        else:
            self.send_message("Expecting Image Input", phone_number)
            return None
    
    def receive_document(self, phone_number):
        """
        Receive and process a document message from a WhatsApp phone number.
        
        Args:
            phone_number (str): The sender's phone number
            
        Returns:
            str: Path to the downloaded document file or None if not found
        """
        data = firebase_client.get_latest_message(phone_number)
        mime_type = self._get_mime_type_from_message(data)
        
        if mime_type and mime_type.split('/')[0] == "application":
            timestamp = (
                data.get('raw_data', {})
                .get('entry', [])[0]
                .get('changes', [])[0]
                .get('value', {})
                .get('messages', [])[0]
                .get('timestamp', None)
            )
            file_id = self._get_document_id(data)
            file_path = download_media(file_id, mime_type, timestamp, phone_number)
            return file_path
        else:
            self.send_message("Expecting Document Input", phone_number)
            return None

# Singleton instance to be imported
whatsapp_service = WhatsAppService() 