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
    question=ICquestion_prompt.Price
    response_format_class=ICexptraction_clases.PriceExtraction
    prompt=ICsystem_prompts.Price
    output=ask_question(client=client, question=question,response_format_class= response_format_class,bool_attribute="has_price", prompt = prompt)
    return output.price

def ask_quantity():
    question=ICquestion_prompt.Quantity
    response_format_class=ICexptraction_clases.QuantityExtraction
    prompt=ICsystem_prompts.Quantity
    output=ask_question(client, question, response_format_class,  bool_attribute="has_quantity", prompt = prompt)
    return output.quantity


def ask_discription():
    question=ICquestion_prompt.Description
    response_format_class=ICexptraction_clases.DescriptionExtraction
    prompt=ICsystem_prompts.Description
    output=ask_question(client, question, response_format_class, bool_attribute="has_description", prompt = prompt)
    return output.description

def ask_brand():
    question=ICquestion_prompt.Brand
    response_format_class=ICexptraction_clases.BrandExtraction
    prompt=ICsystem_prompts.Brand
    output=ask_question(client, question, response_format_class,  bool_attribute="has_brand", prompt = prompt)
    return output.brand

def ask_SKU():
    question=ICquestion_prompt.SKU
    response_format_class=ICexptraction_clases.SKUExtraction
    prompt=ICsystem_prompts.SKU
    output=ask_question(client, question, response_format_class,  bool_attribute="has_SKU", prompt = prompt)
    return output.SKU

def ask_warrenty():
    question=ICquestion_prompt.Warranty
    response_format_class=ICexptraction_clases.WarrantyExtraction
    prompt=ICsystem_prompts.Warranty
    output=ask_question(client, question, response_format_class,  bool_attribute="has_warrenty", prompt = prompt)
    return output.warranty

import time

def ask_imgpath():
    whatsappopration.send_message("Upload Image of your Product")
    time.sleep(20)
    imgpath=whatsappopration.recive_image()
    return imgpath

# -------------------------------------------------------------------------------
# FASHION
# -------------------------------------------------------------------------------

def ask_gender():
    question=ICquestion_prompt.Gender
    response_format_class=ICexptraction_clases.GenderExtraction
    prompt=ICsystem_prompts.Gender
    output=ask_question(client, question, response_format_class,  bool_attribute="has_gender", prompt = prompt)
    return output.gender


def ask_size():
    question = ICquestion_prompt.Size
    response_format_class = ICexptraction_clases.SizeExtraction
    prompt = ICsystem_prompts.Size
    output = ask_question(client, question, response_format_class, bool_attribute="has_size", prompt=prompt)
    return output.size


def ask_material():
    question = ICquestion_prompt.Material
    response_format_class = ICexptraction_clases.MaterialExtraction
    prompt = ICsystem_prompts.Material
    output = ask_question(client, question, response_format_class, bool_attribute="has_material", prompt=prompt)
    return output.material


def ask_color():
    question = ICquestion_prompt.Color
    response_format_class = ICexptraction_clases.ColorExtraction
    prompt = ICsystem_prompts.Color
    output = ask_question(client, question, response_format_class, bool_attribute="has_color", prompt=prompt)
    return output.color


def ask_style():
    question = ICquestion_prompt.Style
    response_format_class = ICexptraction_clases.StyleExtraction
    prompt = ICsystem_prompts.Style
    output = ask_question(client, question, response_format_class, bool_attribute="has_style", prompt=prompt)
    return output.style


def ask_fit():
    question = ICquestion_prompt.Fit
    response_format_class = ICexptraction_clases.FitExtraction
    prompt = ICsystem_prompts.Fit
    output = ask_question(client, question, response_format_class, bool_attribute="has_fit", prompt=prompt)
    return output.fit


def ask_care_instructions():
    question = ICquestion_prompt.CareInstructions
    response_format_class = ICexptraction_clases.CareInstructionsExtraction
    prompt = ICsystem_prompts.CareInstructions
    output = ask_question(client, question, response_format_class, bool_attribute="has_care_instructions", prompt=prompt)
    return output.care_instructions


# -------------------------------------------------------------------------------
# ART AND CRAFT
# -------------------------------------------------------------------------------

def ask_dimensions():
    question = ICquestion_prompt.Dimensions
    response_format_class = ICexptraction_clases.DimensionsExtraction
    prompt = ICsystem_prompts.Dimensions
    output = ask_question(client, question, response_format_class, bool_attribute="has_dimensions", prompt=prompt)
    return output.dimensions


def ask_handmade():
    question = ICquestion_prompt.Handmade
    response_format_class = ICexptraction_clases.HandmadeExtraction
    prompt = ICsystem_prompts.Handmade
    output = ask_question(client, question, response_format_class, bool_attribute="is_handmade", prompt=prompt)
    return output.is_handmade


def ask_customizable():
    question = ICquestion_prompt.Customizable
    response_format_class = ICexptraction_clases.CustomizableExtraction
    prompt = ICsystem_prompts.Customizable
    output = ask_question(client, question, response_format_class, bool_attribute="is_customizable", prompt=prompt)
    return output.is_customizable


def ask_theme():
    question = ICquestion_prompt.Theme
    response_format_class = ICexptraction_clases.ThemeExtraction
    prompt = ICsystem_prompts.Theme
    output = ask_question(client, question, response_format_class, bool_attribute="has_theme", prompt=prompt)
    return output.theme


def ask_usage():
    question = ICquestion_prompt.Usage
    response_format_class = ICexptraction_clases.UsageExtraction
    prompt = ICsystem_prompts.Usage
    output = ask_question(client, question, response_format_class, bool_attribute="has_usage", prompt=prompt)
    return output.usage


# -------------------------------------------------------------------------------
# KIRANA
# -------------------------------------------------------------------------------

def ask_packaging():
    question = ICquestion_prompt.Packaging
    response_format_class = ICexptraction_clases.PackagingExtraction
    prompt = ICsystem_prompts.Packaging
    output = ask_question(client, question, response_format_class, bool_attribute="has_packaging", prompt=prompt)
    return output.packaging


def ask_shelf_life():
    question = ICquestion_prompt.ShelfLife
    response_format_class = ICexptraction_clases.ShelfLifeExtraction
    prompt = ICsystem_prompts.ShelfLife
    output = ask_question(client, question, response_format_class, bool_attribute="has_shelf_life", prompt=prompt)
    return output.shelf_life


def ask_ingredients():
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
    