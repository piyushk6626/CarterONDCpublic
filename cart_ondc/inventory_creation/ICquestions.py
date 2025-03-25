"""
Inventory Creation Questions Module.

This module provides functions to ask questions to users during the inventory creation process.
It handles different types of product attributes and uses AI to extract structured information
from user responses for various product categories.
"""

from pydantic import BaseModel
from openai import OpenAI
from dotenv import load_dotenv
import os
from inventory_creation.ICconversation_handler import ask_question
import inventory_creation.ICquestion_prompt as ICquestion_prompt
import inventory_creation.ICsystem_prompts as ICsystem_prompts
import inventory_creation.ICexptraction_clases as ICexptraction_clases
import inventory_creation.whatsappopration as whatsappopration 
load_dotenv()


api_key=os.getenv("OPENAI_API_KEY")

client = OpenAI(api_key=api_key)

# -------------------------------------------------------------------------------
# COMMON
# -------------------------------------------------------------------------------
    

def ask_price():
    """
    Ask for and extract product price from user response.
    
    Returns:
        float: The extracted price value
    """
    question=ICquestion_prompt.Price
    response_format_class=ICexptraction_clases.PriceExtraction
    prompt=ICsystem_prompts.Price
    output=ask_question(client=client, question=question,response_format_class= response_format_class,bool_attribute="has_price", prompt = prompt)
    return output.price

def ask_quantity():
    """
    Ask for and extract product quantity from user response.
    
    Returns:
        int: The extracted quantity value
    """
    question=ICquestion_prompt.Quantity
    response_format_class=ICexptraction_clases.QuantityExtraction
    prompt=ICsystem_prompts.Quantity
    output=ask_question(client, question, response_format_class,  bool_attribute="has_quantity", prompt = prompt)
    return output.quantity


def ask_discription():
    """
    Ask for and extract product description from user response.
    
    Returns:
        str: The extracted product description
    """
    question=ICquestion_prompt.Description
    response_format_class=ICexptraction_clases.DescriptionExtraction
    prompt=ICsystem_prompts.Description
    output=ask_question(client, question, response_format_class, bool_attribute="has_description", prompt = prompt)
    return output.description

def ask_brand():
    """
    Ask for and extract product brand from user response.
    
    Returns:
        str: The extracted brand name
    """
    question=ICquestion_prompt.Brand
    response_format_class=ICexptraction_clases.BrandExtraction
    prompt=ICsystem_prompts.Brand
    output=ask_question(client, question, response_format_class,  bool_attribute="has_brand", prompt = prompt)
    return output.brand

def ask_SKU():
    """
    Ask for and extract product SKU (Stock Keeping Unit) from user response.
    
    Returns:
        str: The extracted SKU
    """
    question=ICquestion_prompt.SKU
    response_format_class=ICexptraction_clases.SKUExtraction
    prompt=ICsystem_prompts.SKU
    output=ask_question(client, question, response_format_class,  bool_attribute="has_SKU", prompt = prompt)
    return output.SKU

def ask_warrenty():
    """
    Ask for and extract product warranty information from user response.
    
    Returns:
        str: The extracted warranty information
    """
    question=ICquestion_prompt.Warranty
    response_format_class=ICexptraction_clases.WarrantyExtraction
    prompt=ICsystem_prompts.Warranty
    output=ask_question(client, question, response_format_class,  bool_attribute="has_warrenty", prompt = prompt)
    return output.warranty

import time

def ask_imgpath():
    """
    Ask the user to upload a product image and get the image path.
    
    Sends a message to the user requesting an image upload, waits for a response,
    and then receives the image.
    
    Returns:
        str: Path to the uploaded image
    """
    whatsappopration.send_message("Upload Image of your Product")
    time.sleep(20)
    imgpath=whatsappopration.recive_image()
    return imgpath

# -------------------------------------------------------------------------------
# FASHION
# -------------------------------------------------------------------------------

def ask_gender():
    """
    Ask for and extract product gender category from user response for fashion items.
    
    Returns:
        str: The extracted gender information (e.g., Men, Women, Kids, Unisex)
    """
    question=ICquestion_prompt.Gender
    response_format_class=ICexptraction_clases.GenderExtraction
    prompt=ICsystem_prompts.Gender
    output=ask_question(client, question, response_format_class,  bool_attribute="has_gender", prompt = prompt)
    return output.gender


def ask_size():
    """
    Ask for and extract product size information from user response.
    
    Returns:
        str: The extracted size information (e.g., Small, Medium, Large, XL)
    """
    question = ICquestion_prompt.Size
    response_format_class = ICexptraction_clases.SizeExtraction
    prompt = ICsystem_prompts.Size
    output = ask_question(client, question, response_format_class, bool_attribute="has_size", prompt=prompt)
    return output.size


def ask_material():
    """
    Ask for and extract product material information from user response.
    
    Returns:
        str: The extracted material information (e.g., Cotton, Silk, Wool)
    """
    question = ICquestion_prompt.Material
    response_format_class = ICexptraction_clases.MaterialExtraction
    prompt = ICsystem_prompts.Material
    output = ask_question(client, question, response_format_class, bool_attribute="has_material", prompt=prompt)
    return output.material


def ask_color():
    """
    Ask for and extract product color information from user response.
    
    Returns:
        str: The extracted color information
    """
    question = ICquestion_prompt.Color
    response_format_class = ICexptraction_clases.ColorExtraction
    prompt = ICsystem_prompts.Color
    output = ask_question(client, question, response_format_class, bool_attribute="has_color", prompt=prompt)
    return output.color


def ask_style():
    """
    Ask for and extract product style information from user response for fashion items.
    
    Returns:
        str: The extracted style information (e.g., Casual, Formal, Sportswear)
    """
    question = ICquestion_prompt.Style
    response_format_class = ICexptraction_clases.StyleExtraction
    prompt = ICsystem_prompts.Style
    output = ask_question(client, question, response_format_class, bool_attribute="has_style", prompt=prompt)
    return output.style


def ask_fit():
    """
    Ask for and extract product fit information from user response for clothing items.
    
    Returns:
        str: The extracted fit information (e.g., Regular, Slim, Loose)
    """
    question = ICquestion_prompt.Fit
    response_format_class = ICexptraction_clases.FitExtraction
    prompt = ICsystem_prompts.Fit
    output = ask_question(client, question, response_format_class, bool_attribute="has_fit", prompt=prompt)
    return output.fit


def ask_care_instructions():
    """
    Ask for and extract product care instructions from user response.
    
    Returns:
        str: The extracted care instructions
    """
    question = ICquestion_prompt.CareInstructions
    response_format_class = ICexptraction_clases.CareInstructionsExtraction
    prompt = ICsystem_prompts.CareInstructions
    output = ask_question(client, question, response_format_class, bool_attribute="has_care_instructions", prompt=prompt)
    return output.care_instructions


# -------------------------------------------------------------------------------
# ART AND CRAFT
# -------------------------------------------------------------------------------

def ask_dimensions():
    """
    Ask for and extract product dimensions from user response for art and craft items.
    
    Returns:
        str: The extracted dimensions information
    """
    question = ICquestion_prompt.Dimensions
    response_format_class = ICexptraction_clases.DimensionsExtraction
    prompt = ICsystem_prompts.Dimensions
    output = ask_question(client, question, response_format_class, bool_attribute="has_dimensions", prompt=prompt)
    return output.dimensions


def ask_handmade():
    """
    Ask if the product is handmade and extract this information from user response.
    
    Returns:
        bool: True if the product is handmade, False otherwise
    """
    question = ICquestion_prompt.Handmade
    response_format_class = ICexptraction_clases.HandmadeExtraction
    prompt = ICsystem_prompts.Handmade
    output = ask_question(client, question, response_format_class, bool_attribute="is_handmade", prompt=prompt)
    return output.is_handmade


def ask_customizable():
    """
    Ask if the product is customizable and extract this information from user response.
    
    Returns:
        bool: True if the product is customizable, False otherwise
    """
    question = ICquestion_prompt.Customizable
    response_format_class = ICexptraction_clases.CustomizableExtraction
    prompt = ICsystem_prompts.Customizable
    output = ask_question(client, question, response_format_class, bool_attribute="is_customizable", prompt=prompt)
    return output.is_customizable


def ask_theme():
    """
    Ask for and extract product theme information from user response for art and craft items.
    
    Returns:
        str: The extracted theme information (e.g., Traditional, Modern, Abstract)
    """
    question = ICquestion_prompt.Theme
    response_format_class = ICexptraction_clases.ThemeExtraction
    prompt = ICsystem_prompts.Theme
    output = ask_question(client, question, response_format_class, bool_attribute="has_theme", prompt=prompt)
    return output.theme


def ask_usage():
    """
    Ask for and extract product usage information from user response.
    
    Returns:
        str: The extracted usage information (e.g., Decorative, Functional, Both)
    """
    question = ICquestion_prompt.Usage
    response_format_class = ICexptraction_clases.UsageExtraction
    prompt = ICsystem_prompts.Usage
    output = ask_question(client, question, response_format_class, bool_attribute="has_usage", prompt=prompt)
    return output.usage


# -------------------------------------------------------------------------------
# KIRANA
# -------------------------------------------------------------------------------

def ask_packaging():
    """
    Ask for and extract product packaging information from user response.
    
    Returns:
        str: The extracted packaging information
    """
    question = ICquestion_prompt.Packaging
    response_format_class = ICexptraction_clases.PackagingExtraction
    prompt = ICsystem_prompts.Packaging
    output = ask_question(client, question, response_format_class, bool_attribute="has_packaging", prompt=prompt)
    return output.packaging


def ask_shelf_life():
    """
    Ask for and extract product shelf life information from user response.
    
    Returns:
        str: The extracted shelf life information
    """
    question = ICquestion_prompt.ShelfLife
    response_format_class = ICexptraction_clases.ShelfLifeExtraction
    prompt = ICsystem_prompts.ShelfLife
    output = ask_question(client, question, response_format_class, bool_attribute="has_shelf_life", prompt=prompt)
    return output.shelf_life


def ask_ingredients():
    """
    Ask for and extract product ingredients information from user response.
    
    Returns:
        str: The extracted ingredients information
    """
    question = ICquestion_prompt.Ingredients
    response_format_class = ICexptraction_clases.IngredientsExtraction
    prompt = ICsystem_prompts.Ingredients
    output = ask_question(client, question, response_format_class, bool_attribute="has_ingredients", prompt=prompt)
    return output.ingredients


def ask_certifications():
    question = ICquestion_prompt.Certifications
    response_format_class = ICexptraction_clases.CertificationsExtraction
    prompt = ICsystem_prompts.Certifications
    output = ask_question(client, question, response_format_class, bool_attribute="has_certifications", prompt=prompt)
    return output.certifications


# -------------------------------------------------------------------------------
# RESTAURANT
# -------------------------------------------------------------------------------

def ask_type():
    question = ICquestion_prompt.Type
    response_format_class = ICexptraction_clases.TypeExtraction
    prompt = ICsystem_prompts.Type
    output = ask_question(client, question, response_format_class, bool_attribute="has_type", prompt=prompt)
    return output.type


def ask_weight():
    question = ICquestion_prompt.Weight
    response_format_class = ICexptraction_clases.WeightExtraction
    prompt = ICsystem_prompts.Weight
    output = ask_question(client, question, response_format_class, bool_attribute="has_weight", prompt=prompt)
    return output.weight


def ask_allergens():
    question = ICquestion_prompt.Allergens
    response_format_class = ICexptraction_clases.AllergensExtraction
    prompt = ICsystem_prompts.Allergens
    output = ask_question(client, question, response_format_class, bool_attribute="has_allergens", prompt=prompt)
    return output.allergens


def ask_dietary_preferences():
    question = ICquestion_prompt.DietaryPreferences
    response_format_class = ICexptraction_clases.DietaryPreferencesExtraction
    prompt = ICsystem_prompts.DietaryPreferences
    output = ask_question(client, question, response_format_class, bool_attribute="has_dietary_preferences", prompt=prompt)
    return output.dietary_preferences


def ask_storage_instructions():
    question = ICquestion_prompt.StorageInstructions
    response_format_class = ICexptraction_clases.StorageInstructionsExtraction
    prompt = ICsystem_prompts.StorageInstructions
    output = ask_question(client, question, response_format_class, bool_attribute="has_storage_instructions", prompt=prompt)
    return output.storage_instructions


def ask_speciality():
    question = ICquestion_prompt.Speciality
    response_format_class = ICexptraction_clases.SpecialityExtraction
    prompt = ICsystem_prompts.Speciality
    output = ask_question(client, question, response_format_class, bool_attribute="has_speciality", prompt=prompt)
    return output.speciality
    