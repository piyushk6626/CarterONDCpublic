"""
Messaging service for the Cart-ONDC application.

This module handles conversation state management and waiting for user replies
through WhatsApp.
"""

import time
from cart_ondc.core.firebase import firebase_client
from cart_ondc.services.whatsapp_service import whatsapp_service

def wait_for_reply(phone_number, timeout=600):
    """
    Wait for a new message from a specific phone number.
    
    This function continuously checks for new messages from the specified phone number
    until a new message is received or the timeout is reached.
    
    Args:
        phone_number (str): The WhatsApp phone number to wait for a reply from
        timeout (int): Maximum time to wait in seconds (default: 600 seconds / 10 minutes)
        
    Returns:
        str: The text body of the user's reply, or None if no reply is received within the timeout
    """
    start_time = time.time()
    curr = firebase_client.get_latest_message(phone_number)  # Get the current latest message

    while True:
        time.sleep(3)  # Check every 3 seconds for new messages

        latest_message = firebase_client.get_latest_message(phone_number)  # Get the latest message
        
        # Check if we got a new message by comparing with the previous one
        if latest_message != curr:
            user_reply = latest_message.get("text_body", "")  # Extract the reply text
            print(f"User replied: {user_reply}")
            return user_reply

        # Break the loop if timeout is reached
        if time.time() - start_time > timeout:
            print("Timeout reached. No reply received.")
            return None

class ConversationManager:
    """
    Manages conversation state and flow with WhatsApp users.
    
    This class tracks conversation state, sends prompts based on registration flow,
    and processes user responses.
    """
    
    def __init__(self):
        """Initialize the conversation manager with empty state."""
        self.conversations = {}  # Dictionary to track conversation state by phone number
        self.verified_users = {}  # Dictionary to track verified users
    
    def start_conversation(self, phone_number):
        """
        Start a new conversation with a user.
        
        Args:
            phone_number (str): The user's phone number
            
        Returns:
            bool: True if the conversation was started successfully
        """
        if phone_number not in self.conversations:
            self.conversations[phone_number] = {
                'state': 'initial',
                'progress': 0,
                'data': {}
            }
        return True
    
    def get_conversation_state(self, phone_number):
        """
        Get the current conversation state for a user.
        
        Args:
            phone_number (str): The user's phone number
            
        Returns:
            dict: The current conversation state or None if no conversation exists
        """
        return self.conversations.get(phone_number)
    
    def update_conversation(self, phone_number, state=None, progress=None, data=None):
        """
        Update the conversation state for a user.
        
        Args:
            phone_number (str): The user's phone number
            state (str, optional): The new conversation state
            progress (int, optional): The new progress value
            data (dict, optional): Data to add to the conversation
            
        Returns:
            bool: True if the conversation was updated successfully
        """
        if phone_number not in self.conversations:
            self.start_conversation(phone_number)
        
        if state:
            self.conversations[phone_number]['state'] = state
        
        if progress is not None:
            self.conversations[phone_number]['progress'] = progress
        
        if data:
            self.conversations[phone_number]['data'].update(data)
        
        return True
    
    def is_user_verified(self, phone_number):
        """
        Check if a user is verified.
        
        Args:
            phone_number (str): The user's phone number
            
        Returns:
            bool: True if the user is verified, False otherwise
        """
        return self.verified_users.get(phone_number, False)
    
    def set_user_verified(self, phone_number, verified=True):
        """
        Set a user's verification status.
        
        Args:
            phone_number (str): The user's phone number
            verified (bool): The verification status
            
        Returns:
            bool: True if the status was set successfully
        """
        self.verified_users[phone_number] = verified
        return True
    
    def prompt_for_info(self, phone_number, field_name, prompt_message):
        """
        Send a prompt to the user and wait for their reply.
        
        Args:
            phone_number (str): The user's phone number
            field_name (str): The name of the field to collect
            prompt_message (str): The message to send to the user
            
        Returns:
            str: The user's reply or None if no reply was received
        """
        # Send the prompt message
        whatsapp_service.send_message(prompt_message, phone_number)
        
        # Wait for the user's reply
        reply = wait_for_reply(phone_number)
        
        # Update conversation data with the reply
        if reply:
            self.update_conversation(
                phone_number, 
                data={field_name: reply}
            )
        
        return reply

# Singleton instance to be imported
conversation_manager = ConversationManager() 