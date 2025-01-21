import requests
from dotenv import load_dotenv # type: ignore
import os

def download_data(file_id, mime_type, timestamp, phone_number):
    file_name = f"{phone_number}_{timestamp}"
    file_type = mime_type.split("/")[1]
    load_dotenv()
    token = os.getenv("ACCESS_TOKEN")
    version = "v16.0"
    media_url = f"https://graph.facebook.com/{version}/{file_id}"
    
    file_path = f"{file_name}.{file_type}"
    database_folder = os.path.join("database", phone_number)
    if not os.path.exists(database_folder):
        os.makedirs(database_folder)
    save_path = os.path.join(database_folder, file_path)

    headers = {
        "Authorization": f"Bearer {token}"
    }

    response = requests.get(media_url, headers=headers)
    if response.status_code == 200:
        file_url = response.json().get("url")
        if not file_url:
            print("No URL found in the response.")
            return 1
        
        file_response = requests.get(file_url, headers=headers)
        if file_response.status_code == 200:
            with open(save_path, "wb") as file:
                file.write(file_response.content)
            print(f"Image downloaded successfully and saved as {save_path}")
            return save_path
        else:
            print(f"Failed to download file: {file_response.status_code}")
            return 1
    else:
        print(f"Failed to retrieve media URL: {response.status_code}")
        return 1
