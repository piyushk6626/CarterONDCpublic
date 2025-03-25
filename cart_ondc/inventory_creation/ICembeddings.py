"""
Inventory Creation Embeddings Module

This module provides functions for creating and managing embeddings for inventory items,
which can be used for semantic search and recommendations.
"""

from openai import OpenAI
from dotenv import load_dotenv
import os
import logging

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Load environment variables
load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")

# Initialize OpenAI client
client = OpenAI(api_key=api_key)
    
def get_embedding(text, model="text-embedding-3-small"):
    """
    Get vector embeddings for the given text using OpenAI's embedding model.
    
    Args:
        text (str): The text to generate embeddings for.
        model (str): The embedding model to use.
        
    Returns:
        list: The embedding vector.
    """
    try:
        text = text.replace("\n", " ")
        return client.embeddings.create(input=[text], model=model).data[0].embedding
    except Exception as e:
        logger.error(f"Error generating embeddings: {e}")
        return None

def create_embeddings(text, model="text-embedding-3-small"):
    """
    Create embeddings for a product description or title.
    
    Args:
        text (str): The text to generate embeddings for (typically product name + description).
        model (str): The embedding model to use.
        
    Returns:
        list: The embedding vector or None if an error occurs.
    """
    try:
        if not text:
            logger.warning("Empty text provided for embeddings")
            return None
            
        embeddings = get_embedding(text, model=model)
        logger.info(f"Successfully created embeddings for text: {text[:50]}...")
        return embeddings
    except Exception as e:
        logger.error(f"Failed to create embeddings: {e}")
        return None