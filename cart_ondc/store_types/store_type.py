"""
Store type module for the Cart-ONDC application.

This module handles store type selection and provides templates for
different types of stores available for registration.
"""

class StoreType:
    """Manages store type selection and templates."""
    
    @staticmethod
    def select_store_type():
        """
        Get the initial message for store type selection.
        
        Returns:
            str: A formatted message listing available store types
        """
        message = (
            "Welcome to Cart-ONDC! Please select your store type:\n\n"
            "1. Kiriana Store (Grocery & Packaged Food)\n"
            "2. Clothing Store\n"
            "3. Handicraft Shop\n"
            "4. Restaurant / Sweet & Snack Shop\n\n"
            "Reply with the number or name of your store type."
        )
        return message
    
    @staticmethod
    def get_registration_flow(store_type):
        """
        Get the registration flow for a specific store type.
        
        Args:
            store_type (str): The type of store
            
        Returns:
            generator: A generator yielding messages to prompt for registration data
            
        Raises:
            ValueError: If the store type is not supported
        """
        store_type = store_type.lower()
        
        if store_type == "1" or store_type == "kiriana" or store_type == "kiriana store":
            return StoreType._kiriana_registration_flow()
        elif store_type == "2" or store_type == "clothing" or store_type == "clothing store":
            return StoreType._clothing_registration_flow()
        elif store_type == "3" or store_type == "handicraft" or store_type == "handicraft shop":
            return StoreType._handicraft_registration_flow()
        elif store_type == "4" or store_type == "restaurant" or store_type == "resturant" or store_type == "sweet and snack shop":
            return StoreType._restaurant_registration_flow()
        else:
            raise ValueError(f"Unsupported store type: {store_type}")
    
    @staticmethod
    def _kiriana_registration_flow():
        """
        Generate prompts for Kiriana store registration.
        
        Yields:
            str: Message prompts for each step of registration
        """
        yield "Let's register your Kiriana Store. Please provide the following information:"
        yield "Please enter your name:"
        yield "Please enter your date of birth (DD/MM/YYYY):"
        yield "Please enter your PAN card number:"
        yield "Please enter your GST number:"
        yield "Please enter your complete address:"
        yield "Please enter your business name:"
        yield "Please enter your trade license number:"
        yield "Please enter your Udyam registration number:"
        yield "Please enter your bank account number:"
        yield "Please enter your bank's IFSC code:"
        yield "Please enter your UPI ID:"
        yield "Thank you for registering your Kiriana Store! Your information has been submitted for verification."
    
    @staticmethod
    def _clothing_registration_flow():
        """
        Generate prompts for Clothing store registration.
        
        Yields:
            str: Message prompts for each step of registration
        """
        yield "Let's register your Clothing Store. Please provide the following information:"
        yield "Please enter your name:"
        yield "Please enter your date of birth (DD/MM/YYYY):"
        yield "Please enter your PAN card number:"
        yield "Please enter your GST number:"
        yield "Please enter your complete address:"
        yield "Please enter your business name:"
        yield "Please enter your trade license number:"
        yield "Please enter your Udyam registration number:"
        yield "Please enter your bank account number:"
        yield "Please enter your bank's IFSC code:"
        yield "Please enter your UPI ID:"
        yield "Thank you for registering your Clothing Store! Your information has been submitted for verification."
    
    @staticmethod
    def _handicraft_registration_flow():
        """
        Generate prompts for Handicraft shop registration.
        
        Yields:
            str: Message prompts for each step of registration
        """
        yield "Let's register your Handicraft Shop. Please provide the following information:"
        yield "Please enter your name:"
        yield "Please enter your date of birth (DD/MM/YYYY):"
        yield "Please enter your PAN card number:"
        yield "Please enter your GST number:"
        yield "Please enter your complete address:"
        yield "Please enter your business name:"
        yield "Please enter your trade license number:"
        yield "Please enter your Udyam registration number:"
        yield "Please enter your bank account number:"
        yield "Please enter your bank's IFSC code:"
        yield "Please enter your UPI ID:"
        yield "Thank you for registering your Handicraft Shop! Your information has been submitted for verification."
    
    @staticmethod
    def _restaurant_registration_flow():
        """
        Generate prompts for Restaurant registration.
        
        Yields:
            str: Message prompts for each step of registration
        """
        yield "Let's register your Restaurant. Please provide the following information:"
        yield "Please enter your name:"
        yield "Please enter your date of birth (DD/MM/YYYY):"
        yield "Please enter your PAN card number:"
        yield "Please enter your GST number:"
        yield "Please enter your complete address:"
        yield "Please enter your business name:"
        yield "Please enter your trade license number:"
        yield "Please enter your Udyam registration number:"
        yield "Please enter your bank account number:"
        yield "Please enter your bank's IFSC code:"
        yield "Please enter your UPI ID:"
        yield "Please enter your FSSAI license number:"
        yield "Thank you for registering your Restaurant! Your information has been submitted for verification."

# Singleton instance to be imported
store_type_manager = StoreType() 