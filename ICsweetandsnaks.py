import inventory_creation.ICquestions as ICquestions
import uuid
import inventory_creation.ICdiscriptiongenrator as ICdiscriptiongenrator
import inventory_creation.ICembeddings as ICembeddings
import inventory_creation.ICdatabase_opration as ICdatabase_opration
class SweetAndSnaks:
    def __init__(self, description=None, price=None, quantity=None, imgpath=None, id=None):
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
        self.title = str(ICquestions.ask_discription())
        self.price = ICquestions.ask_price()
        self.quantity = ICquestions.ask_quantity()        
        self.Type = str(ICquestions.ask_type())
        self.Ingredients = str(ICquestions.ask_ingredients())
        self.ShelfLife = str(ICquestions.ask_shelf_life())
        self.Weight = str(ICquestions.ask_weight())
        self.imgpath = str(ICquestions.ask_imgpath())
        
    
    def generate_id(self):
        self.id = uuid.uuid4().hex[:40]
    
    def write_description(self):
        title =f"the title is {str(self.title)} the Type is {str(self.Type)} the main Ingredients is {str(self.Ingredients)} the ShelfLife is {str(self.ShelfLife)} the Weight is {str(self.Weight)} "
        
        imgpath = str(self.imgpath)
        self.description = str(ICdiscriptiongenrator.write_Discription_for_artandcraft(title, imgpath))
    def generate_embedding(self):
        self.embedding = ICembeddings.get_embedding(self.description)
    
    def to_dict(self):
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