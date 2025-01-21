import firebase_admin
from firebase_admin import credentials, firestore
from google.cloud.firestore_v1.vector import Vector



# Initialize Firebase Admin SDK only if it's not already initialized

if not firebase_admin._apps:
    cred = credentials.Certificate("auth.json")
    firebase_admin.initialize_app(cred)

# Initialize Firestore client
db = firestore.client()



def add_product(data):
    """
    Adds a WhatsApp message document to the Firestore 'WhatsAppMessages' collection.
    The message ID is used as the document ID, and the 'embeddings' field is replaced 
    with a vector representation if it exists.
    """
    print("HELLO")
    try:
        # Extract the document ID (message ID) from the data
        pid = data.get("id")
        if not pid:
            raise ValueError("The data does not contain a valid 'id' field.")

        # If 'embeddings' exists, process it and update the data
        if 'embeddings' in data:
            embeddings = data.pop('embeddings')  # Remove the old 'embeddings' field
            data['vectorized_embeddings'] = Vector(embeddings)  # Replace with processed vector

        # Add the document to the Firestore collection
        collection = db.collection("Products")
        collection.document(pid).set(data)  # Use `pid` as the document ID

        print(f"Document added successfully with ID: {pid}")
    except Exception as e:
        print(f"An error occurred while adding the WhatsApp message: {e}")
