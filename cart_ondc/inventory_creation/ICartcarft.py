"""
Art and Craft Product Management Module.

This module handles the creation and management of art and craft products in the inventory,
including generating descriptions, embeddings, and storing in the database.
"""

import inventory_creation.ICquestions as ICquestions
import uuid
import inventory_creation.ICdiscriptiongenrator as ICdiscriptiongenrator
import inventory_creation.ICembeddings as ICembeddings
import inventory_creation.ICdatabase_opration as ICdatabase_opration

class ArtAndCraft:
    """
    Art and Craft product class for managing handicraft items in the inventory.
    
    This class handles the creation, description generation, embedding creation,
    and storage of art and craft products in the database.
    """
    
    def __init__(self, description=None, price=None, quantity=None, imgpath=None, id=None):
        """
        Initialize an Art and Craft product instance.
        
        Args:
            description (str, optional): Product description
            price (float, optional): Product price
            quantity (int, optional): Available quantity
            imgpath (str, optional): Path to product image
            id (str, optional): Product ID
        """
        self.description = description
        self.price = price
        self.quantity = quantity
        self.imgpath = imgpath
        self.id = id
        self.title = None
        self.meterial = None
        self.theme = None
        self.embedding = None
        self.category="Art and craft"
    
    def setvalues(self):
        """
        Set product values by asking questions to the user.
        
        Uses interactive questions to gather product information including title,
        price, quantity, material, image path, usage, and theme.
        """
        self.title = str(ICquestions.ask_discription())
        self.price = ICquestions.ask_price()
        self.quantity = ICquestions.ask_quantity()
        self.meterial = str(ICquestions.ask_material())
        self.imgpath = str(ICquestions.ask_imgpath())
        self.Usage = str(ICquestions.ask_usage())
        self.theme = str(ICquestions.ask_theme())
        
    def generate_id(self):
        """Generate a unique ID for the art and craft product."""
        self.id = uuid.uuid4().hex[:40]
    
    def write_description(self):
        """
        Generate a product description using the title, material, usage, and theme.
        
        Uses the description generator to create a detailed product description.
        """
        title =f"the title is {str(self.title)} the metrial is {str(self.meterial)} the usage is {str(self.Usage)} the theme is {str(self.theme)}"
        
        imgpath = str(self.imgpath)
        self.description = str(ICdiscriptiongenrator.write_Discription_for_artandcraft(title, imgpath))
    
    def generate_embedding(self):
        """Generate embedding vector for the product description."""
        self.embedding = ICembeddings.get_embedding(self.description)
    
    def to_dict(self):
        """
        Convert the art and craft product to a dictionary.
        
        Returns:
            dict: Dictionary representation of the art and craft product
        """
        return {
            "id": self.id,
            "description": self.description,
            "title": self.title,
            "price": self.price,
            "quantity": self.quantity,
            "imgpath": self.imgpath,
            "meterial": self.meterial,
            "usage": self.Usage,
            "theme": self.theme,
            "category":self.category,
            "embedding": self.embedding
        }
    
    def create_product(self):
        """
        Create a complete art and craft product by executing the full workflow.
        
        This method performs all steps to create a product:
        1. Generate a unique ID
        2. Set values by asking the user
        3. Write a description
        4. Generate embeddings
        5. Store in the database
        
        Returns:
            dict: The created product as a dictionary
        """
        self.generate_id()
        self.setvalues()
        self.write_description()
        self.generate_embedding()
        ProductDict= self.to_dict()
        ICdatabase_opration.add_product(ProductDict)
        return ProductDict
        
if __name__ == "__main__":
    product = ArtAndCraft()
    product_dict = product.create_product()
    print(product_dict)