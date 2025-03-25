"""
Base registration module for the Cart-ONDC application.

This module provides a base class for store registration with common fields and methods
that are shared across all store types.
"""

from abc import ABC, abstractmethod
from cart_ondc.services.messaging import conversation_manager
from cart_ondc.core.database import db_manager

class BaseRegistration(ABC):
    """
    Base class for store registration.
    
    This abstract class defines common fields and methods for all store types
    and requires concrete implementations to specify their unique fields.
    """
    
    # Common fields for all store types
    COMMON_FIELDS = [
        'name',
        'dob',
        'pancard',
        'gst_number',
        'address',
        'business_name',
        'trade_license',
        'udyam',
        'account_number',
        'ifsc_code',
        'upi_id',
        'phoneNumber'
    ]
    
    def __init__(self, phone_number):
        """
        Initialize registration for a specific phone number.
        
        Args:
            phone_number (str): The phone number to register
        """
        self.phone_number = phone_number
        self.registration_data = {}
        conversation_manager.start_conversation(phone_number)
    
    @property
    @abstractmethod
    def store_type(self):
        """Get the store type name."""
        pass
    
    @property
    @abstractmethod
    def required_fields(self):
        """Get the required fields for this store type."""
        pass
    
    @abstractmethod
    def store_data(self):
        """Store the registration data in the database."""
        pass
    
    def get_prompt_message(self, field_name):
        """
        Get the prompt message for a specific field.
        
        Args:
            field_name (str): The field to get the prompt for
            
        Returns:
            str: The prompt message
        """
        prompts = {
            'name': "Please enter your name:",
            'dob': "Please enter your date of birth:",
            'pancard': "Please enter your PAN card number:",
            'gst_number': "Please enter your GST number:",
            'address': "Please enter your address:",
            'business_name': "Please enter your business name:",
            'trade_license': "Please enter your trade license number:",
            'udyam': "Please enter your Udyam number:",
            'account_number': "Please enter your account number:",
            'ifsc_code': "Please enter your IFSC code:",
            'upi_id': "Please enter your UPI ID:",
            'fssai_number': "Please enter your FSSAI number:",
            'phoneNumber': "Please enter your phone number:"
        }
        
        return prompts.get(field_name, f"Please enter your {field_name}:")
    
    def register(self):
        """
        Run the registration process for this store type.
        
        This method will prompt the user for all required fields and store
        the data in the database upon completion.
        
        Returns:
            bool: True if registration was successful
        """
        # Ensure the registration data includes the phone number
        self.registration_data['phoneNumber'] = self.phone_number
        
        # Get the current conversation state
        state = conversation_manager.get_conversation_state(self.phone_number)
        progress = state.get('progress', 0) if state else 0
        
        # Continue from where we left off
        for i, field in enumerate(self.required_fields[progress:], start=progress):
            # Skip fields that are already collected
            if field in self.registration_data and self.registration_data[field]:
                continue
            
            # Prompt for the field
            prompt_message = self.get_prompt_message(field)
            reply = conversation_manager.prompt_for_info(self.phone_number, field, prompt_message)
            
            # If no reply, break and save progress
            if not reply:
                conversation_manager.update_conversation(self.phone_number, progress=i)
                return False
            
            # Store the reply
            self.registration_data[field] = reply
            conversation_manager.update_conversation(self.phone_number, progress=i+1)
        
        # All fields collected, store the data
        result = self.store_data()
        
        if result:
            # Set the user as verified in the database
            db_manager.set_verified(self.phone_number, True, self.store_type)
            # Reset the conversation for this user
            conversation_manager.update_conversation(self.phone_number, state='completed', progress=0)
        
        return result 