import inventory_creation.ICquestions as ICquestions 
import uuid
import inventory_creation.ICdiscriptiongenrator as ICdiscriptiongenrator 
import inventory_creation.ICembeddings as ICembeddings
import inventory_creation.ICdatabase_opration as ICdatabase_opration

class Fashion:
    def __init__(self, description=None, price=None, quantity=None, imgpath=None, id=None):
        self.description = description
        self.price = price
        self.quantity = quantity
        self.imgpath = imgpath
        self.id = id
        self.title = None
        self.gender = None
        self.embedding = None
        self.category="Fashion"
    
    def setvalues(self):
        self.title = str(ICquestions.ask_discription())
        self.price = ICquestions.ask_price()
        self.quantity = ICquestions.ask_quantity()
        self.gender = str(ICquestions.ask_gender())
        self.imgpath = str(ICquestions.ask_imgpath())
        
    def generate_id(self):
        self.id = uuid.uuid4().hex[:40]
    
    def write_description(self):
        title = str(self.title)
        imgpath = str(self.imgpath)
        self.description = str(ICdiscriptiongenrator.write_Discription_for_fashion(title, imgpath))
    
    def to_dict(self):
        return {
            "id": self.id,
            "description": self.description,
            "title": self.title,
            "price": self.price,
            "quantity": self.quantity,
            "imgpath": self.imgpath,
            "gender": self.gender,
            "category" : self.category,
            "embedding": self.embedding
        }
    def generate_embedding(self):
        self.embedding = ICembeddings.get_embedding(self.description)
    
    def create_product(self):
        self.generate_id()
        self.setvalues()
        self.write_description()
        self.generate_embedding()
        ProductDict= self.to_dict()
        ICdatabase_opration.add_product(ProductDict)
        return ProductDict
        
if __name__ == "__main__":
    product = Fashion()
    product_dict = product.create_product()
    print(product_dict)