"""
Kiriana store registration module for the Cart-ONDC application.

This module handles registration for Kiriana stores (grocery and packaged food),
including collecting and validating store-specific information.
"""

from cart_ondc.registration.base_registration import BaseRegistration
from cart_ondc.core.database import db_manager

class KirianaRegistration(BaseRegistration):
    """
    Kiriana store registration handler.
    
    Handles the registration process for Kiriana stores, which includes
    basic store information without any specialized licenses.
    """
    
    @property
    def store_type(self):
        """
        Get the store type name.
        
        Returns:
            str: The store type name
        """
        return "kiriana"
    
    @property
    def required_fields(self):
        """
        Get the required fields for Kiriana store registration.
        
        Returns:
            list: List of required field names
        """
        return self.COMMON_FIELDS  # No additional fields for Kiriana stores
    
    def store_data(self):
        """
        Store the Kiriana registration data in the database.
        
        This method calls the database manager to store the collected registration data.
        
        Returns:
            bool: True if the data was stored successfully
        """
        return db_manager.store_kiriana_data(self.registration_data)
    
    def validate_gst(self, gst_number):
        """
        Validate a GST number for Kiriana stores.
        
        Args:
            gst_number (str): The GST number to validate
            
        Returns:
            bool: True if the GST number is valid
        """
        # TODO: Implement actual GST validation logic
        # This is a placeholder for actual validation logic
        if len(gst_number) < 15:
            return False
        return True
    
    def validate_pan(self, pan_number):
        """
        Validate a PAN card number.
        
        Args:
            pan_number (str): The PAN card number to validate
            
        Returns:
            bool: True if the PAN card number is valid
        """
        # TODO: Implement actual PAN card validation logic
        # This is a placeholder for actual validation logic
        if len(pan_number) != 10:
            return False
        return True 