"""
Inventory API for the Cart-ONDC application.

This module provides the API endpoints for handling inventory-related operations,
including product creation, updating, and management.
"""

from flask import request, jsonify, Blueprint
import uuid
from datetime import datetime
from cart_ondc.inventory_creation.ICdatabase_opration import add_product, get_product
from cart_ondc.inventory_creation.ICdiscriptiongenrator import generate_product_description
from cart_ondc.inventory_creation.ICembeddings import create_embeddings

# Create a Blueprint for the inventory routes
inventory_bp = Blueprint('inventory', __name__)

@inventory_bp.route('/product', methods=['POST'])
def create_product():
    """
    Create a new product in the inventory.
    
    Expects a JSON payload with product details.
    
    Returns:
        dict: A JSON response with the created product ID and status
    """
    try:
        data = request.json
        
        # Validate required fields
        required_fields = ['name', 'category', 'price']
        for field in required_fields:
            if field not in data:
                return jsonify({
                    'status': 'error',
                    'message': f'Missing required field: {field}'
                }), 400
        
        # Generate a unique product ID if not provided
        if 'id' not in data:
            data['id'] = str(uuid.uuid4())
        
        # Add timestamp
        data['created_at'] = datetime.now().isoformat()
        
        # Generate product description if not provided
        if 'description' not in data:
            data['description'] = generate_product_description(
                data.get('name', ''),
                data.get('category', ''),
                data.get('attributes', {})
            )
        
        # Generate embeddings for search
        embeddings = create_embeddings(data.get('name', '') + ' ' + data.get('description', ''))
        if embeddings:
            data['embeddings'] = embeddings
        
        # Add product to database
        success = add_product(data)
        
        if success:
            return jsonify({
                'status': 'success',
                'message': 'Product created successfully',
                'product_id': data['id']
            }), 201
        else:
            return jsonify({
                'status': 'error',
                'message': 'Failed to create product'
            }), 500
            
    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': str(e)
        }), 500

@inventory_bp.route('/product/<product_id>', methods=['GET'])
def get_product_details(product_id):
    """
    Get details for a specific product by ID.
    
    Args:
        product_id (str): The ID of the product to retrieve
        
    Returns:
        dict: A JSON response with the product details
    """
    try:
        product = get_product(product_id)
        
        if product:
            return jsonify({
                'status': 'success',
                'product': product
            }), 200
        else:
            return jsonify({
                'status': 'error',
                'message': 'Product not found'
            }), 404
            
    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': str(e)
        }), 500

# Function to register the blueprint with the Flask app
def register_inventory(app):
    """
    Register the inventory blueprint with the Flask app.
    
    Args:
        app (Flask): The Flask app
    """
    app.register_blueprint(inventory_bp, url_prefix='/inventory') 