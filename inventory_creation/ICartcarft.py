import inventory_creation.ICquestions as ICquestions
import uuid
import inventory_creation.ICdiscriptiongenrator as ICdiscriptiongenrator
import inventory_creation.ICembeddings as ICembeddings
import inventory_creation.ICdatabase_opration as ICdatabase_opration
class ArtAndCraft:
    def __init__(self, description=None, price=None, quantity=None, imgpath=None, id=None):
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
        self.title = str(ICquestions.ask_discription())
        self.price = ICquestions.ask_price()
        self.quantity = ICquestions.ask_quantity()
        self.meterial = str(ICquestions.ask_material())
        self.imgpath = str(ICquestions.ask_imgpath())
        self.Usage = str(ICquestions.ask_usage())
        self.theme = str(ICquestions.ask_theme())
        
    def generate_id(self):
        self.id = uuid.uuid4().hex[:40]
    
    def write_description(self):
        title =f"the title is {str(self.title)} the metrial is {str(self.meterial)} the usage is {str(self.Usage)} the theme is {str(self.theme)}"
        
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
            "meterial": self.meterial,
            "usage": self.Usage,
            "theme": self.theme,
            "category":self.category,
            "embedding": self.embedding
        }
    
    def create_product(self):
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