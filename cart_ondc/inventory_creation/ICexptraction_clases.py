from pydantic import BaseModel
from typing import Optional

# -------------------------------------------------------------------------------
# COMMON
# -------------------------------------------------------------------------------

class PriceExtraction(BaseModel):
    has_price: bool
    price: Optional[float] = None  
    
class QuantityExtraction(BaseModel):
    has_quantity: bool
    quantity: Optional[int] = None

class DescriptionExtraction(BaseModel):
    has_description: bool
    description: Optional[str] = None

class BrandExtraction(BaseModel):
    has_brand: bool
    brand: Optional[str] = None

class SKUExtraction(BaseModel):
    has_sku: bool
    sku: Optional[str] = None

class WarrantyExtraction(BaseModel):
    has_warranty: bool
    warranty: Optional[str] = None

# -------------------------------------------------------------------------------
# FASHION
# -------------------------------------------------------------------------------

class GenderExtraction(BaseModel):
    has_gender: bool
    gender: Optional[str] = None

class SizeExtraction(BaseModel):
    has_size: bool
    size: Optional[str] = None

class MaterialExtraction(BaseModel):
    has_material: bool
    material: Optional[str] = None

class ColorExtraction(BaseModel):
    has_color: bool
    color: Optional[str] = None

class StyleExtraction(BaseModel):
    has_style: bool
    style: Optional[str] = None

class OccasionExtraction(BaseModel):
    has_occasion: bool
    occasion: Optional[str] = None

class FitExtraction(BaseModel):
    has_fit: bool
    fit: Optional[str] = None

class CareInstructionsExtraction(BaseModel):
    has_care_instructions: bool
    care_instructions: Optional[str] = None

# -------------------------------------------------------------------------------
# ART AND CRAFT
# -------------------------------------------------------------------------------

class DimensionsExtraction(BaseModel):
    has_dimensions: bool
    dimensions: Optional[str] = None

class HandmadeExtraction(BaseModel):
    is_handmade: bool

class CustomizableExtraction(BaseModel):
    is_customizable: bool

class ThemeExtraction(BaseModel):
    has_theme: bool
    theme: Optional[str] = None

class UsageExtraction(BaseModel):
    has_usage: bool
    usage: Optional[str] = None

# -------------------------------------------------------------------------------
# KIRANA
# -------------------------------------------------------------------------------

class PackagingExtraction(BaseModel):
    has_packaging: bool
    packaging: Optional[str] = None

class ShelfLifeExtraction(BaseModel):
    has_shelf_life: bool
    shelf_life: Optional[str] = None

class IngredientsExtraction(BaseModel):
    has_ingredients: bool
    ingredients: Optional[str] = None

class CertificationsExtraction(BaseModel):
    has_certifications: bool
    certifications: Optional[str] = None

# -------------------------------------------------------------------------------
# RESTAURANT
# -------------------------------------------------------------------------------

class TypeExtraction(BaseModel):
    has_type: bool
    type: Optional[str] = None

class WeightExtraction(BaseModel):
    has_weight: bool
    weight: Optional[str] = None

class AllergensExtraction(BaseModel):
    has_allergens: bool
    allergens: Optional[str] = None

class DietaryPreferencesExtraction(BaseModel):
    has_dietary_preferences: bool
    dietary_preferences: Optional[str] = None

class StorageInstructionsExtraction(BaseModel):
    has_storage_instructions: bool
    storage_instructions: Optional[str] = None

class SpecialityExtraction(BaseModel):
    has_speciality: bool
    speciality: Optional[str] = None

