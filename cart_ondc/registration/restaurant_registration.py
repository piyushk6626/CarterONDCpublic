"""
Restaurant registration module for the Cart-ONDC application.

This module handles registration for Restaurants and Food service businesses,
including collecting and validating FSSAI license and other store-specific information.
"""

from cart_ondc.registration.base_registration import BaseRegistration
from cart_ondc.core.database import db_manager

class RestaurantRegistration(BaseRegistration):
    """
    Restaurant registration handler.
    
    Handles the registration process for Restaurants and Food service businesses,
    which includes basic store information plus FSSAI licensing.
    """
    
    @property
    def store_type(self):
        """
        Get the store type name.
        
        Returns:
            str: The store type name
        """
        return "restaurant"
    
    @property
    def required_fields(self):
        """
        Get the required fields for Restaurant registration.
        
        Returns:
            list: List of required field names
        """
        # Include common fields plus FSSAI license number
        return self.COMMON_FIELDS + ['fssai_number']
    
    def store_data(self):
        """
        Store the Restaurant registration data in the database.
        
        This method calls the database manager to store the collected registration data.
        
        Returns:
            bool: True if the data was stored successfully
        """
        return db_manager.store_restaurant_data(self.registration_data)
    
    def validate_fssai(self, fssai_number):
        """
        Validate an FSSAI license number.
        
        Args:
            fssai_number (str): The FSSAI license number to validate
            
        Returns:
            bool: True if the FSSAI license number is valid
        """
        # TODO: Implement actual FSSAI validation logic
        # This is a placeholder for actual validation logic
        if len(fssai_number) < 14:
            return False
        return True
    
    def validate_gst(self, gst_number):
        """
        Validate a GST number for Restaurants.
        
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