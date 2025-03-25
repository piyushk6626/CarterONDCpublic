"""
Main entry point for the Cart-ONDC application.

This module initializes and runs the Flask application.
"""

from cart_ondc.api.app import app

if __name__ == "__main__":
    # Run the application in debug mode
    app.run(debug=True, host="0.0.0.0", port=5000)
