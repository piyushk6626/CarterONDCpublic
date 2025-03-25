"""
Main Flask application for the Cart-ONDC service.

This module initializes the Flask application and registers all required
blueprints and routes.
"""

from flask import Flask, jsonify
from cart_ondc.api.webhook import register_webhook

def create_app():
    """
    Create and configure the Flask application.
    
    Returns:
        Flask: The configured Flask application
    """
    app = Flask(__name__)
    
    # Register blueprints
    register_webhook(app)
    
    # Root route for health check
    @app.route('/', methods=['GET'])
    def health_check():
        """
        Health check endpoint.
        
        Returns:
            dict: A JSON response indicating the service is running
        """
        return jsonify({
            "status": "healthy",
            "service": "Cart-ONDC API",
            "version": "1.0.0"
        })
    
    return app

# Application factory pattern
app = create_app() 