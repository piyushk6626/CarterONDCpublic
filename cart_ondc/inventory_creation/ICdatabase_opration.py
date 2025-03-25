"""
Inventory Creation Database Operations Module

This module provides functions for interacting with the Firestore database
for inventory management operations, including adding and retrieving products.
"""

import firebase_admin
from firebase_admin import credentials, firestore
from google.cloud.firestore_v1.vector import Vector
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Initialize Firebase Admin SDK only if it's not already initialized
if not firebase_admin._apps:
    # Use environment variables for configuration path
    firebase_config_path = os.getenv("FIREBASE_CONFIG_PATH", "auth.json")
    cred = credentials.Certificate(firebase_config_path)
    firebase_admin.initialize_app(cred)

# Initialize Firestore client
db = firestore.client()


def add_product(data):
    """
    Adds a product document to the Firestore 'Products' collection.
    
    Args:
        data (dict): The product data dictionary containing product information.
                    Must include an 'id' field to be used as document ID.
                    May include an 'embeddings' field which will be converted to a Vector.
    
    Returns:
        bool: True if the operation was successful, False otherwise.
    
    Raises:
        ValueError: If the data does not contain a valid 'id' field.
    """
    try:
        # Extract the document ID (product ID) from the data
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

        print(f"Product added successfully with ID: {pid}")
        return True
    except Exception as e:
        print(f"An error occurred while adding the product: {e}")
        return False


def get_product(product_id):
    """
    Retrieves a product from the Firestore 'Products' collection.
    
    Args:
        product_id (str): The ID of the product to retrieve.
        
    Returns:
        dict: The product data if found, None otherwise.
    """
    try:
        product_ref = db.collection("Products").document(product_id)
        product_doc = product_ref.get()
        
        if product_doc.exists:
            return product_doc.to_dict()
        else:
            print(f"Product with ID {product_id} not found.")
            return None
    except Exception as e:
        print(f"An error occurred while retrieving the product: {e}")
        return None
