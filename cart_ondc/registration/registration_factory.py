"""
Registration factory module for the Cart-ONDC application.

This module provides a factory for creating the appropriate registration handler
based on the store type selected by the user.
"""

from cart_ondc.registration.kiriana_registration import KirianaRegistration
from cart_ondc.registration.restaurant_registration import RestaurantRegistration

class RegistrationFactory:
    """
    Factory for creating registration handlers.
    
    This class creates the appropriate registration handler based on the store type,
    allowing for a unified interface to handle different registration flows.
    """
    
    @staticmethod
    def create_registration(store_type, phone_number):
        """
        Create a registration handler for the specified store type.
        
        Args:
            store_type (str): The type of store to register
            phone_number (str): The phone number of the user
            
        Returns:
            BaseRegistration: A registration handler for the specified store type
            
        Raises:
            ValueError: If the store type is not supported
        """
        store_type = store_type.lower()
        
        if store_type == "kiriana" or store_type == "1" or store_type == "kiriana store":
            return KirianaRegistration(phone_number)
        elif store_type == "restaurant" or store_type == "4" or store_type == "resturant":
            return RestaurantRegistration(phone_number)
        # Add other store types as needed
        else:
            raise ValueError(f"Unsupported store type: {store_type}")

# Example usage:
# registration = RegistrationFactory.create_registration("kiriana", "1234567890")
# registration.register() 