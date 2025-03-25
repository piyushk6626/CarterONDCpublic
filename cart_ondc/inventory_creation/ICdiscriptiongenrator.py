"""
Inventory Creation Description Generator Module

This module provides functions for generating product descriptions using AI.
It includes specialized functions for different product categories like fashion,
art and craft, packed food, and sweets and snacks.
"""

import base64
import os
import logging
from openai import OpenAI
from dotenv import load_dotenv
import cart_ondc.inventory_creation.ICsystem_prompts as ICsystem_prompts

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Load environment variables
load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")
client = OpenAI(api_key=api_key)

def generate_product_description(product_name, category, attributes=None):
    """
    Generate a product description based on name, category and attributes.
    
    Args:
        product_name (str): The name of the product.
        category (str): The category of the product (e.g., 'fashion', 'food').
        attributes (dict, optional): Additional product attributes.
    
    Returns:
        str: Generated product description.
    """
    try:
        if attributes is None:
            attributes = {}
            
        # Convert attributes to a string
        attr_text = ""
        for key, value in attributes.items():
            attr_text += f"{key}: {value}, "
        
        # Create prompt for text-based description
        prompt = f"Generate a detailed and appealing product description for a {category} product named '{product_name}' with the following attributes: {attr_text}"
        
        # Generate description using OpenAI
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "You are a professional product copywriter. Create concise, appealing product descriptions that highlight key features and benefits."},
                {"role": "user", "content": prompt}
            ]
        )
        
        description = response.choices[0].message.content
        logger.info(f"Generated description for product: {product_name}")
        return description
        
    except Exception as e:
        logger.error(f"Error generating product description: {e}")
        return f"Product: {product_name}. Category: {category}."

def write_Discription_for_fashion(title, img_path):
    """
    Generate a description for a fashion product using image and title.
    
    Args:
        title (str): The title or name of the fashion item.
        img_path (str): Path to the product image.
    
    Returns:
        str: Generated fashion product description.
    """
    try:
        response = process_image_with_openai(
            image_path=img_path,
            description=title,
            prompt=ICsystem_prompts.DiscriptionGenrator,
            client=client
        )
        return response
    except Exception as e:
        logger.error(f"Error generating fashion description: {e}")
        return generate_product_description(title, "fashion")
    
def write_Discription_for_artandcraft(title, img_path):
    """
    Generate a description for an art and craft product using image and title.
    
    Args:
        title (str): The title or name of the art/craft item.
        img_path (str): Path to the product image.
    
    Returns:
        str: Generated art and craft product description.
    """
    try:
        response = process_image_with_openai(
            image_path=img_path,
            description=title,
            prompt=ICsystem_prompts.ArtAndCraftDescriptionGenerator,
            client=client
        )
        return response
    except Exception as e:
        logger.error(f"Error generating art and craft description: {e}")
        return generate_product_description(title, "art and craft")

def write_Discription_for_Packed_food(title, img_path):
    """
    Generate a description for packed food using image and title.
    
    Args:
        title (str): The title or name of the packed food item.
        img_path (str): Path to the product image.
    
    Returns:
        str: Generated packed food description.
    """
    try:
        response = process_image_with_openai(
            image_path=img_path,
            description=title,
            prompt=ICsystem_prompts.pakedfoodDescriptionGenerator,
            client=client
        )
        return response
    except Exception as e:
        logger.error(f"Error generating packed food description: {e}")
        return generate_product_description(title, "packed food")

def write_Discription_for_sweets_and_snacks(title, img_path):
    """
    Generate a description for sweets and snacks using image and title.
    
    Args:
        title (str): The title or name of the sweet/snack item.
        img_path (str): Path to the product image.
    
    Returns:
        str: Generated sweets and snacks description.
    """
    try:
        response = process_image_with_openai(
            image_path=img_path,
            description=title,
            prompt=ICsystem_prompts.SweetsDescriptionGenerator,
            client=client
        )
        return response
    except Exception as e:
        logger.error(f"Error generating sweets description: {e}")
        return generate_product_description(title, "sweets and snacks")

def process_image_with_openai(image_path, description, prompt, client, model="gpt-4o-mini"):
    """
    Process an image using OpenAI's API to generate a description.
    
    Args:
        image_path (str): Path to the image file.
        description (str): Description or title of the image.
        prompt (str): The prompt to send to the API.
        client: OpenAI client instance.
        model (str): Model to use for processing (default: "gpt-4o-mini").
    
    Returns:
        str: The generated description from the API.
    """
    try:
        # Function to encode the image
        def encode_image(image_path):
            with open(image_path, "rb") as image_file:
                return base64.b64encode(image_file.read()).decode("utf-8")
        
        # Get base64 encoded image
        base64_image = encode_image(image_path)
        
        # Create API request
        response = client.chat.completions.create(
            model=model,
            messages=[
                {
                    "role": "user",
                    "content": [
                        {
                            "type": "text",
                            "text": prompt + description,
                        },
                        {
                            "type": "image_url",
                            "image_url": {"url": f"data:image/jpeg;base64,{base64_image}"},
                        },
                    ],
                }
            ],
        )
        
        return response.choices[0].message.content
    except Exception as e:
        logger.error(f"Error processing image with OpenAI: {e}")
        raise e

# Example usage
if __name__ == "__main__":
    
    response=write_Discription_for_fashion(img_path="D:\DEV\ONDC\CarterONDC\img.jpg",title="tshirt")
    
    print(response)
