import requests, json, os, sqlite3
from dotenv import load_dotenv # type: ignore

load_dotenv()
accessToken = os.getenv("ACCESS_TOKEN")
version = os.getenv("VERSION")
phoneNumberId = os.getenv("PHONE_NUMBER_ID")

def send_message(phoneNumber, message):
    url = f"https://graph.facebook.com/{version}/{phoneNumberId}/messages"
    
    headers = {
        "Authorization": "Bearer " + accessToken,
        "Content-Type": "application/json",
    }
    
    data = {
        "messaging_product": "whatsapp",
        "to": phoneNumber,
        "type": "text",
        "text": {"body": message},
    }
    
    response = requests.post(url, headers=headers, data=json.dumps(data))

    if response.status_code == 200:
        print(f"Message sent successfully: {message}")
    else:
        print(f"Failed to send message. Status Code: {response.status_code}, Response: {response.text}")

def get_message(phoneNumber):
    conn = sqlite3.connect('whatsapp.db')
    c = conn.cursor()
    c.execute("SELECT data FROM messages WHERE phoneNumber = ? ORDER BY timestamp DESC LIMIT 1", (phoneNumber,))
    res = c.fetchone()
    if res:
        return json.loads(res[0])
    else:
        return None
