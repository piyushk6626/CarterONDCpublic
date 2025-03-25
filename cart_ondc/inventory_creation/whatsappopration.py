import requests
import json
from dotenv import load_dotenv # type: ignore
import os
import firebase_admin
from firebase_admin import credentials, firestore
import downloadData

# Load environment variables from .env file
load_dotenv()



# Initialize Firebase Admin SDK only if it's not already initialized
if not firebase_admin._apps:
    cred = credentials.Certificate("auth.json")
    firebase_admin.initialize_app(cred)

# Initialize Firestore client
db = firestore.client()




def get_latest_message(phone_number):
    """
    Retrieves and prints the JSON of the latest message from the given phone number.
    Args:
       
    """
    try:
        # Query the Firestore collection to get the latest message from the specified phone number
        collection = db.collection("WhatsAppMessages")
        query = (
            collection
            .where("contact_wa_id", "==", phone_number)  # Filter messages from the given phone number
            .order_by("timestamp", direction=firestore.Query.DESCENDING)  # Sort by timestamp (latest first)
            .limit(1)  # Limit the query to one document
        )
        
        # Execute the query
        results = query.stream()

        # Iterate through the results
        for result in results:
            message_data = result.to_dict()  # Convert Firestore document to a dictionary
            # print("Latest message JSON:")
            # print(message_data)  # Print the full JSON object of the latest message
            return message_data

        # If no message is found
        print(f"No messages found for the phone number: {phone_number}")
        return None

    except Exception as e:
        print(f"An error occurred while retrieving the message: {e}")
        return None
    
def send_message(message, phone_number):

    url = "https://graph.facebook.com/v21.0/479971375209028/messages"  # Replace with your phone number ID
    

    access_token = os.getenv("ACCESS_TOKEN") 
    # Headers for the request
    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json"
    }

    # Payload (Message data)
    data = {
        "messaging_product": "whatsapp",
        "to": phone_number,  # Use the dynamic phone number passed to the function
        "type": "text",  # Send a simple text message
        "text": {
            "body": message  # Custom message passed to the function
        }
    }

    # Send the POST request to the WhatsApp API
    response = requests.post(url, headers=headers, data=json.dumps(data))

    # Check if the request was successful
    if response.status_code == 200:
        print(f"Message sent successfully: {message}")
    else:
        print(f"Failed to send message. Status Code: {response.status_code}, Response: {response.text}")


def get_mime_type_from_message(message_data):
    """
    Extracts the MIME type from the raw_data of the latest message.
    
    Args:
        message_data (dict): The dictionary returned by get_latest_message.
        
    Returns:
        str: The MIME type of the message (e.g., "audio/ogg; codecs=opus") or None if not found.
    """
    try:
        # Navigate to the MIME type field in the raw_data for audio
        mime_type = (
            message_data.get('raw_data', {})
            .get('entry', [])[0]
            .get('changes', [])[0]
            .get('value', {})
            .get('messages', [])[0]
            .get('audio', {})
            .get('mime_type', None)
        )

        if mime_type is None:
            mime_type = (
            message_data.get('raw_data', {})
            .get('entry', [])[0]
            .get('changes', [])[0]
            .get('value', {})
            .get('messages', [])[0]
            .get('image', {})
            .get('mime_type', None)
         )
            
        if mime_type is None:
            mime_type = (
            message_data.get('raw_data', {})
            .get('entry', [])[0]
            .get('changes', [])[0]
            .get('value', {})
            .get('messages', [])[0]
            .get('document', {})
            .get('mime_type', None)
         )
            


        return mime_type
    except Exception as e:
        print(f"An error occurred while extracting the MIME type: {e}")
        return None
    
def get_audio_id(message_data):
    """
    Extracts and returns the `id` inside the `audio` field from the given message data.
    
    Args:
        message_data (dict): The dictionary containing the message data.
        
    Returns:
        str: The ID of the audio message or None if not found.
    """
    try:
        # Extract the audio id field
        audio_id = (
            message_data.get('raw_data', {})
            .get('entry', [])[0]
            .get('changes', [])[0]
            .get('value', {})
            .get('messages', [])[0]
            .get('audio', {})
            .get('id', None)
        )
        return audio_id
    except Exception as e:
        print(f"An error occurred while extracting the audio id: {e}")
        return None
def get_image_id(message_data):
    """
    Extracts and returns the `id` inside the `image` field from the given message data.
    
    Args:
        message_data (dict): The dictionary containing the message data.
        
    Returns:
        str: The ID of the image or None if not found.
    """
    try:
        # Extract the image id field
        image_id = (
            message_data.get('raw_data', {})
            .get('entry', [])[0]
            .get('changes', [])[0]
            .get('value', {})
            .get('messages', [])[0]
            .get('image', {})
            .get('id', None)
        )
        
        return image_id
    
    except Exception as e:
        print(f"An error occurred while extracting the image id: {e}")
        return None

def get_doc_id(message_data):
    """
    Extracts and returns the `id` inside the `image` field from the given message data.
    
    Args:
        message_data (dict): The dictionary containing the message data.
        
    Returns:
        str: The ID of the image or None if not found.
    """
    try:
        # Extract the image id field
        doc_id = (
            message_data.get('raw_data', {})
            .get('entry', [])[0]
            .get('changes', [])[0]
            .get('value', {})
            .get('messages', [])[0]
            .get('document', {})
            .get('id', None)
        )
        
        return doc_id
    
    except Exception as e:
        print(f"An error occurred while extracting the image id: {e}")
        return None


def recive_message(phone_number):

    data = get_latest_message(phone_number)
    type = get_mime_type_from_message(data)
    if type is None:
        text_body = data.get('text_body', None)
        print(data)
        print(f"Rply was {text_body}")
        return text_body
    else:
        send_message(f"Expecting Text Input", phone_number)
    # print(data)
    # return message

def recive_audio(phone_number):
    # SAVE IMAGE AND RETURN IMAGE PATH
    data = get_latest_message(phone_number)
    type = get_mime_type_from_message(data)
    if type == "audio/ogg; codecs=opus":
        timestamp = (
            data.get('raw_data', {})
            .get('entry', [])[0]
            .get('changes', [])[0]
            .get('value', {})
            .get('messages', [])[0]
            .get('timestamp', None)  # Extract timestamp field
        )
        mime_type = "audio/ogg"
        file_id = get_audio_id(data)
        file_path = downloadData.download_data(file_id, mime_type, timestamp, phone_number)
        return file_path
    else:
        send_message(f"Expecting Audio Input", phone_number)

def recive_image(phone_number):
    # SAVE IMAGE AND RETURN IMAGE PATH
    data = get_latest_message(phone_number)
    type = get_mime_type_from_message(data)
    print(type)
    if type.split('/')[0] == "image":
        timestamp = (
            data.get('raw_data', {})
            .get('entry', [])[0]
            .get('changes', [])[0]
            .get('value', {})
            .get('messages', [])[0]
            .get('timestamp', None)  # Extract timestamp field
        )
        mime_type = type
        file_id = get_image_id(data)
        file_path = downloadData.download_data(file_id, mime_type, timestamp, phone_number)
        return file_path
    else:
        send_message(f"Expecting Image Input", phone_number)

def recive_document(phone_number):
    # SAVE IMAGE AND RETURN IMAGE PATH
    data = get_latest_message(phone_number)
    type = get_mime_type_from_message(data)
    print(type)
    if type.split('/')[0] == "application":
        timestamp = (
            data.get('raw_data', {})
            .get('entry', [])[0]
            .get('changes', [])[0]
            .get('value', {})
            .get('messages', [])[0]
            .get('timestamp', None)  # Extract timestamp field
        )
        mime_type = type
        file_id = get_doc_id(data)
        file_path = downloadData.download_data(file_id, mime_type, timestamp, phone_number)
        return file_path
    else:
        send_message(f"Expecting Document Input", phone_number)

