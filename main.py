from flask import Flask, request, jsonify
import firebase_admin
from firebase_admin import credentials, firestore
import json
import os
from google.cloud.firestore_v1.vector import Vector
import datetime
import checkVerified
import storeType
import resturantRegistration
import clothingRegistration
import handicraftRegistration
import kirianaRegistration
import whatsappopration as whtsapp
import time
import ICFashion

# Initialize Firebase Admin SDK only if it's not already initialized
if not firebase_admin._apps:
    cred = credentials.Certificate("auth.json")
    firebase_admin.initialize_app(cred)

# Initialize Firestore client
db = firestore.client()



def add_product(data):
    print("HELLO")
    """
    Adds a WhatsApp message document to the Firestore 'WhatsAppMessages' collection.
    The message ID is used as the document ID, and the entire JSON is stored.
    """
    try:
        # Extract message details
        messaging_product = data.get('entry', [])[0].get('changes', [])[0].get('value', {}).get('messaging_product', None)
        phone_number_id = data.get('entry', [])[0].get('changes', [])[0].get('value', {}).get('metadata', {}).get('phone_number_id', None)
        display_phone_number = data.get('entry', [])[0].get('changes', [])[0].get('value', {}).get('metadata', {}).get('display_phone_number', None)
        contact_wa_id = data.get('entry', [])[0].get('changes', [])[0].get('value', {}).get('contacts', [])[0].get('wa_id', None)
        contact_name = data.get('entry', [])[0].get('changes', [])[0].get('value', {}).get('contacts', [])[0].get('profile', {}).get('name', None)
        message_id = data.get('entry', [])[0].get('changes', [])[0].get('value', {}).get('messages', [])[0].get('id', None)
        timestamp = (data.get('entry', [])[0].get('changes', [])[0].get('value', {}).get('messages', [])[0].get('timestamp', None))  # Extract timestamp field )
        text_body = data.get('entry', [])[0].get('changes', [])[0].get('value', {}).get('messages', [])[0].get('text', {}).get('body', None)
        
        # Convert timestamp to human-readable format
        # timestamp = datetime.datetime.fromtimestamp(int(timestamp)).strftime('%Y-%m-%d %H:%M:%S') if timestamp else None

        # Prepare Firestore document
        doc = {
            "messaging_product": messaging_product,
            "phone_number_id": phone_number_id,
            "display_phone_number": display_phone_number,
            "contact_wa_id": contact_wa_id,
            "contact_name": contact_name,
            "message_id": message_id,
            "timestamp": timestamp,
            "text_body": text_body,
            "raw_data": data  # Store the full JSON object for reference
        }

        print(doc)

        

        # Add the document to the Firestore collection, using `message_id` as the document ID
        collection = db.collection("WhatsAppMessages")
        collection.document(message_id).set(doc)  # Use `message_id` as the primary key

        print(f"Message from {contact_wa_id} added successfully with ID: {message_id}")
    except Exception as e:
        print(f"An error occurred while adding the WhatsApp message: {e}")

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



app = Flask(__name__)

# def waitforresponse(phone_number):

def wait_for_reply(phone_number, timeout=600):
    """
    Waits for a new message from the specified phone number.
    
    
    
    Returns:
        str: The text body of the user's reply, or None if no reply is received within the timeout.
    """
    start_time = time.time()
    curr = get_latest_message(phone_number)  # Get the current latest message

    while True:
        time.sleep(3)  # Check every 3 seconds for new messages

        latest_message = get_latest_message(phone_number)  # Get the latest message
        if latest_message != curr:  # Check if a new message is received
            user_reply = latest_message.get("text_body", "")  # Extract the reply text
            print(f"User replied: {user_reply}")
            return user_reply

        # Break the loop if timeout is reached
        if time.time() - start_time > timeout:
            print("Timeout reached. No reply received.")
            return None

    

firstmsg = {}
dic = {}
@app.route('/', defaults={'path': ''}, methods=['POST'])
@app.route('/<path:path>', methods=['POST'])


def handle_post(path):
    print("-------------- New Request POST --------------")
    
    # print("Headers:", request.headers)
    data  = request.json
    
    
    try:
        
        contact_wa_id = None
        contact_wa_id = data.get('entry', [])[0].get('changes', [])[0].get('value', {}).get('messages', [])[0].get('from', None)
        if contact_wa_id is None:
            raise ValueError("Couldnt Read Phone Number")
        phone_number = contact_wa_id
        
        add_product(data)
        print (contact_wa_id)
        # wait_for_reply(contact_wa_id)
        verified = checkVerified.isVerified(phone_number)
        if (contact_wa_id not in firstmsg or firstmsg[contact_wa_id] < 13) and not verified :
            if (contact_wa_id not in  firstmsg):
                whtsapp.send_message(storeType.selectStoreType(), contact_wa_id)
                firstmsg[contact_wa_id] = 0
            else:
                firstmsg[contact_wa_id] += 1

            if (contact_wa_id not in dic):
                dic[contact_wa_id] = {}
            
            print(f"Waiting for a reply from {contact_wa_id}...")
            time.sleep(2)
            curr = wait_for_reply(phone_number) # which type did they choose
            lst = None
            if curr == "1" or curr.lower()  == "kiriana store":
                lst = kirianaRegistration.inputDataKiriana
            elif curr == "2" or curr.lower() == "clothing store":
                lst = clothingRegistration.inputDataClothing
            elif curr == "3" or curr.lower() == "handicraft shop":
                lst = handicraftRegistration.inputDataHandicraft
            elif curr == "2" or curr.lower() ==  "resturant":
                lst = resturantRegistration.inputDataresturant


            gen = storeType.optionSelected(curr)

            inx = 0
            
            if curr == "1" or curr.lower()  == "kiriana store":
                for msg in gen:
                    whtsapp.send_message(msg, phone_number)
                    inp = wait_for_reply(phone_number)
                    dic[contact_wa_id][kirianaRegistration.inputDataKiriana[inx]] = inp
                    inx += 1
                kirianaRegistration.store_data_kiriana(dic[contact_wa_id])

            elif curr == "2" or curr.lower() == "clothing store":
                for msg in gen:
                    whtsapp.send_message(msg, phone_number)
                    inp = wait_for_reply(phone_number)
                    dic[contact_wa_id][clothingRegistration.inputDataclothing[inx]] = inp
                    inx += 1
                clothingRegistration.store_data_clothing(dic[contact_wa_id])

            elif curr == "3" or curr.lower() == "handicraft shop":
                for msg in gen:
                    whtsapp.send_message(msg, phone_number)
                    inp = wait_for_reply(phone_number)
                    dic[contact_wa_id][handicraftRegistration.inputDatahandicraft[inx]] = inp
                    inx += 1
                handicraftRegistration.store_data_handicraft(dic[contact_wa_id])

            elif curr == "2" or curr.lower() ==  "resturant":
                for msg in gen:
                    whtsapp.send_message(msg, phone_number)
                    inp = wait_for_reply(phone_number)
                    dic[contact_wa_id][resturantRegistration.inputDataresturant[inx]] = inp
                    inx += 1
                resturantRegistration.store_data_resturant(dic[contact_wa_id])
            
            checkVerified.setVerified(False, phone_number)
            time.sleep(5)
        else:
            pass
            # wait_for_reply(phone_number)
            # for i in range(5):
            #     product = ICFashion.Fashion()
            #     product.create_product()



        
        

    except Exception as e:
        print(f"RROR: {e}")
    

  
    except:
        pass

    
   

    return jsonify({"message": "Thank you for the message"})




@app.route('/', defaults={'path': ''}, methods=['GET'])
@app.route('/<path:path>', methods=['GET'])
def handle_get(path):
    # Parse the query parameters
    mode = request.args.get("hub.mode")
    token = request.args.get("hub.verify_token")
    challenge = request.args.get("hub.challenge")

    print("-------------- New Request GET --------------")
    
    # print("Headers:", request.headers)
    data  = request.json
    # print("Body:", data)

    

   

    add_product(data)
    get_latest_message(phone_number)



    # Check if a token and mode is in the query string of the request
    if mode and token:
        # Check the mode and token sent is correct
        if mode == "subscribe" and token == "12345":
            # Respond with the challenge token from the request
            print("WEBHOOK_VERIFIED")
            return challenge, 200
        else:
            print("Responding with 403 Forbidden")
            # Respond with '403 Forbidden' if verify tokens do not match
            return "Forbidden", 403
    else:
        print("Replying Thank you.")
        return jsonify({"message": "Thank you for the message"})

if __name__ == '__main__':
    port = 3000
    app.run(port=port, debug=True)
