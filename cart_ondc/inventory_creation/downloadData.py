"""
Download Data Module for Inventory Creation

This module provides functions for downloading media files from WhatsApp API
and storing them locally for inventory creation processes.
"""

import requests
import os
import logging
from dotenv import load_dotenv

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Load environment variables
load_dotenv()

def download_data(file_id, mime_type, timestamp, phone_number):
    """
    Downloads a file from the WhatsApp API using the file ID and saves it locally.

    Args:
        file_id (str): The ID of the file to download from WhatsApp API.
        mime_type (str): The MIME type of the file (e.g., 'image/jpeg').
        timestamp (str): The timestamp when the file was sent, used for naming.
        phone_number (str): The phone number of the sender, used for organizing files.

    Returns:
        str: The path to the saved file on success, or 1 if download failed.
    """
    try:
        # Generate file name and determine file type
        file_name = f"{phone_number}_{timestamp}"
        file_type = mime_type.split("/")[1]
        
        # Get access token from environment variables
        token = os.getenv("ACCESS_TOKEN")
        if not token:
            logger.error("ACCESS_TOKEN not found in environment variables")
            return 1
            
        # Construct the media URL
        version = "v16.0"
        media_url = f"https://graph.facebook.com/{version}/{file_id}"
        
        # Create the directory structure if it doesn't exist
        file_path = f"{file_name}.{file_type}"
        database_folder = os.path.join("database", phone_number)
        if not os.path.exists(database_folder):
            os.makedirs(database_folder)
        save_path = os.path.join(database_folder, file_path)

        # Set up the authorization header
        headers = {
            "Authorization": f"Bearer {token}"
        }

        # First request to get the file URL
        response = requests.get(media_url, headers=headers)
        if response.status_code == 200:
            file_url = response.json().get("url")
            if not file_url:
                logger.error("No URL found in the response.")
                return 1
            
            # Second request to download the actual file
            file_response = requests.get(file_url, headers=headers)
            if file_response.status_code == 200:
                with open(save_path, "wb") as file:
                    file.write(file_response.content)
                logger.info(f"File downloaded successfully and saved as {save_path}")
                return save_path
            else:
                logger.error(f"Failed to download file: {file_response.status_code}")
                return 1
        else:
            logger.error(f"Failed to retrieve media URL: {response.status_code}")
            return 1
    except Exception as e:
        logger.exception(f"Error downloading data: {e}")
        return 1
