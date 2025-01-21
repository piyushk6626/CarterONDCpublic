import inventory_creation.ICquestions as ICquestions
import uuid
import inventory_creation.ICdiscriptiongenrator as ICdiscriptiongenrator
import inventory_creation.ICembeddings as ICembeddings
import inventory_creation.ICdatabase_opration as ICdatabase_opration
class Packedfood:
    def __init__(self, description=None, price=None, quantity=None, imgpath=None, id=None):
        self.description = description
        self.price = price
        self.quantity = quantity
        self.imgpath = imgpath
        self.id = id
        self.title = None
        self.Size = None
        self.Packaging = None
        self.embedding = None
        self.category="Packed Food"
    
    def setvalues(self):
        self.title = str(ICquestions.ask_discription())
        self.price = ICquestions.ask_price()
        self.quantity = ICquestions.ask_quantity()        
        self.Size = str(ICquestions.ask_size())
        self.Packaging = str(ICquestions.ask_packaging())
        self.imgpath = str(ICquestions.ask_imgpath())
    
    def generate_id(self):
        self.id = uuid.uuid4().hex[:40]
    
    def write_description(self):
        title =f"the title is {str(self.title)} the size is {str(self.Size)} the packeging is {str(self.Packaging)} "
        
        imgpath = str(self.imgpath)
        self.description = str(ICdiscriptiongenrator.write_Discription_for_Packed_food(title, imgpath))
    
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
            "Size": self.Size,
            "Packaging": self.Packaging,
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
    product = Packedfood()
    product_dict = product.create_product()
    print(product_dict)