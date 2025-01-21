# import firebase_admin
# from firebase_admin import credentials, firestore
# import json
# import os
# from google.cloud.firestore_v1.vector import Vector

# # Initialize Firebase Admin SDK
# cred = credentials.Certificate("auth.json")
# firebase_admin.initialize_app(cred)

# # Initialize Firestore client
# db = firestore.client()

# def read_json_file(file_path):
#     """Reads a JSON file and returns its content."""
#     try:
#         with open(file_path, 'r', encoding='utf-8') as file:
#             return json.load(file)
#     except json.JSONDecodeError as e:
#         print(f"Error decoding JSON from file {file_path}: {e}")
#     except Exception as e:
#         print(f"An error occurred while reading file {file_path}: {e}")
#     return None

# def add_whatsapp_message(data):
#     """
#     Adds a WhatsApp message document to the Firestore 'WhatsAppMessages' collection.
#     The message ID is used as the document ID, and the entire JSON is stored.
#     """
#     try:
#         # Extract message details
#         messaging_product = data.get('entry', [])[0].get('changes', [])[0].get('value', {}).get('messaging_product', None)
#         phone_number_id = data.get('entry', [])[0].get('changes', [])[0].get('value', {}).get('metadata', {}).get('phone_number_id', None)
#         display_phone_number = data.get('entry', [])[0].get('changes', [])[0].get('value', {}).get('metadata', {}).get('display_phone_number', None)
#         contact_wa_id = data.get('entry', [])[0].get('changes', [])[0].get('value', {}).get('contacts', [])[0].get('wa_id', None)
#         contact_name = data.get('entry', [])[0].get('changes', [])[0].get('value', {}).get('contacts', [])[0].get('profile', {}).get('name', None)
#         message_id = data.get('entry', [])[0].get('changes', [])[0].get('value', {}).get('messages', [])[0].get('id', None)
#         timestamp = data.get('entry', [])[0].get('changes', [])[0].get('value', {}).get('messages', [])[0].get('timestamp', None)
#         text_body = data.get('entry', [])[0].get('changes', [])[0].get('value', {}).get('messages', [])[0].get('text', {}).get('body', None)
        
#         # Convert timestamp to human-readable format
#         timestamp = datetime.fromtimestamp(int(timestamp)).strftime('%Y-%m-%d %H:%M:%S') if timestamp else None

#         # Prepare Firestore document
#         doc = {
#             "messaging_product": messaging_product,
#             "phone_number_id": phone_number_id,
#             "display_phone_number": display_phone_number,
#             "contact_wa_id": contact_wa_id,
#             "contact_name": contact_name,
#             "message_id": message_id,
#             "timestamp": timestamp,
#             "text_body": text_body,
#             "raw_data": data  # Store the full JSON object for reference
#         }

#         # Add the document to the Firestore collection, using `message_id` as the document ID
#         collection = db.collection("WhatsAppMessages")
#         collection.document(message_id).set(doc)  # Use `message_id` as the primary key

#         print(f"Message from {contact_wa_id} added successfully with ID: {message_id}")
#     except Exception as e:
#         print(f"An error occurred while adding the WhatsApp message: {e}")
        
# def process_json_files_in_folder(folder_path):
#     """Processes all JSON files in the specified folder."""
#     if not os.path.exists(folder_path):
#         print(f"The folder path '{folder_path}' does not exist.")
#         return

#     for filename in os.listdir(folder_path):
#         if filename.endswith('.json'):
#             file_path = os.path.join(folder_path, filename)
#             data = read_json_file(file_path)
#             if data:
#                 add_product(data)
#             else:
#                 print(f"Failed to process file: {filename}")

# # Path to the folder containing JSON files
# folder_path = os.path.join('finaldatabase','embeddings_20250118_031830','Bewakoof')
# process_json_files_in_folder(folder_path)
