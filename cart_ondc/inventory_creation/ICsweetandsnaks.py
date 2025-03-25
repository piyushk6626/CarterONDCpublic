"""
Sweet and Snacks Product Management Module.

This module handles the creation and management of sweet and snack products in the inventory,
including generating descriptions, embeddings, and storing in the database.
"""

import inventory_creation.ICquestions as ICquestions
import uuid
import inventory_creation.ICdiscriptiongenrator as ICdiscriptiongenrator
import inventory_creation.ICembeddings as ICembeddings
import inventory_creation.ICdatabase_opration as ICdatabase_opration

class SweetAndSnaks:
    """
    Sweet and Snacks product class for managing sweet and snack items in the inventory.
    
    This class handles the creation, description generation, embedding creation,
    and storage of sweet and snack products in the database.
    """
    
    def __init__(self, description=None, price=None, quantity=None, imgpath=None, id=None):
        """
        Initialize a Sweet and Snacks product instance.
        
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
        self.Type = None
        self.Ingredients = None
        self.ShelfLife= None
        self.Weight= None
        self.Occasion = None
        self.embedding = None
        self.category="Sweet and snacks"
    
    def setvalues(self):
        """
        Set product values by asking questions to the user.
        
        Uses interactive questions to gather product information including title,
        price, quantity, type, ingredients, shelf life, weight, and image path.
        """
        self.title = str(ICquestions.ask_discription())
        self.price = ICquestions.ask_price()
        self.quantity = ICquestions.ask_quantity()        
        self.Type = str(ICquestions.ask_type())
        self.Ingredients = str(ICquestions.ask_ingredients())
        self.ShelfLife = str(ICquestions.ask_shelf_life())
        self.Weight = str(ICquestions.ask_weight())
        self.imgpath = str(ICquestions.ask_imgpath())
        
    
    def generate_id(self):
        """Generate a unique ID for the sweet and snacks product."""
        self.id = uuid.uuid4().hex[:40]
    
    def write_description(self):
        """
        Generate a product description using the title, type, ingredients, shelf life, and weight.
        
        Uses the description generator to create a detailed product description.
        """
        title =f"the title is {str(self.title)} the Type is {str(self.Type)} the main Ingredients is {str(self.Ingredients)} the ShelfLife is {str(self.ShelfLife)} the Weight is {str(self.Weight)} "
        
        imgpath = str(self.imgpath)
        self.description = str(ICdiscriptiongenrator.write_Discription_for_artandcraft(title, imgpath))
        
    def generate_embedding(self):
        """Generate embedding vector for the product description."""
        self.embedding = ICembeddings.get_embedding(self.description)
    
    def to_dict(self):
        """
        Convert the sweet and snacks product to a dictionary.
        
        Returns:
            dict: Dictionary representation of the sweet and snacks product
        """
        return {
            "id": self.id,
            "description": self.description,
            "title": self.title,
            "price": self.price,
            "quantity": self.quantity,
            "imgpath": self.imgpath,
            "Type": self.Type,
            "Ingredients": self.Ingredients,
            "ShelfLife": self.ShelfLife,
            "Weight": self.Weight,
            "category":self.category,
            "embedding": self.embedding
        }
    
    def create_product(self):
        """
        Generates a product from user input and returns it as a dictionary

        The generated product contains the following keys:
        - id: a unique identifier for the product
        - description: a human-readable description of the product
        - title: the title of the product
        - price: the price of the product
        - quantity: the quantity of the product
        - imgpath: the path to an image of the product
        - Type: the type of the product
        - Ingredients: the ingredients of the product
        - ShelfLife: the shelf life of the product
        - Weight: the weight of the product
        - category: the category of the product (in this case, always 'Sweet and snacks')
        - embedding: an embedding of the product description

        Returns:
            dict: A dictionary containing the generated product
        """
        self.generate_id()
        self.setvalues()
        self.write_description()
        self.generate_embedding()
        ProductDict= self.to_dict()
        ICdatabase_opration.add_product(ProductDict)
        return ProductDict
        
        
if __name__ == "__main__":
    product = SweetAndSnaks()
    product_dict = product.create_product()
    print(product_dict)