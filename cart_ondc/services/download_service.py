"""
Download service for the Cart-ONDC application.

This module handles downloading media files from WhatsApp Business API,
including audio, images, and documents.
"""

import requests
import os
import json
from dotenv import load_dotenv
import mimetypes
from pathlib import Path

# Load environment variables from .env file
load_dotenv()

def download_media(file_id, mime_type, timestamp, phone_number):
    """
    Download media file from WhatsApp Cloud API.
    
    Args:
        file_id (str): The ID of the file to download
        mime_type (str): The MIME type of the file
        timestamp (str): The timestamp of the message
        phone_number (str): The sender's phone number
        
    Returns:
        str: Path to the downloaded file or None if download failed
    """
    try:
        # Get the access token from environment variables
        access_token = os.getenv("ACCESS_TOKEN")
        
        # API endpoint for retrieving media URL
        url = f"https://graph.facebook.com/v21.0/{file_id}"
        
        # Headers for the request
        headers = {
            "Authorization": f"Bearer {access_token}"
        }
        
        # Send request to get the media URL
        response = requests.get(url, headers=headers)
        
        if response.status_code != 200:
            print(f"Failed to get media URL. Status Code: {response.status_code}, Response: {response.text}")
            return None
        
        # Parse the response to get the media URL
        media_data = response.json()
        media_url = media_data.get("url")
        
        if not media_url:
            print("Media URL not found in the response")
            return None
        
        # Determine file extension based on MIME type
        extension = _get_extension_from_mime_type(mime_type)
        
        # Create the media directory if it doesn't exist
        media_dir = Path("media")
        media_dir.mkdir(exist_ok=True)
        
        # Create a filename using timestamp, phone number, and extension
        filename = f"{timestamp}_{phone_number}{extension}"
        file_path = media_dir / filename
        
        # Download the media file
        media_response = requests.get(media_url, headers=headers)
        
        if media_response.status_code != 200:
            print(f"Failed to download media. Status Code: {media_response.status_code}")
            return None
        
        # Save the media file
        with open(file_path, "wb") as f:
            f.write(media_response.content)
        
        print(f"Media downloaded successfully: {file_path}")
        return str(file_path)
    
    except Exception as e:
        print(f"An error occurred while downloading media: {e}")
        return None

def _get_extension_from_mime_type(mime_type):
    """
    Determine file extension from MIME type.
    
    Args:
        mime_type (str): The MIME type
        
    Returns:
        str: The file extension including the dot
    """
    # Extract the primary MIME type
    if mime_type:
        primary_mime = mime_type.split(';')[0].strip()
    else:
        return ".bin"  # Default binary extension
    
    # Get the extension from the MIME type
    extension = mimetypes.guess_extension(primary_mime)
    
    # If no extension is found, use defaults based on MIME type category
    if not extension:
        mime_category = primary_mime.split('/')[0]
        if mime_category == "audio":
            extension = ".ogg"
        elif mime_category == "image":
            extension = ".jpg"
        elif mime_category == "video":
            extension = ".mp4"
        elif mime_category == "application":
            extension = ".pdf"
        else:
            extension = ".bin"
    
    return extension 