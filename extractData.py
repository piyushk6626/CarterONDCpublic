import json

def extract_message_data(json_data):
    data = json.loads(json_data)

    if "statuses" in data:
        return None

    entry = data.get("entry", [])[0]
    change = entry.get("changes", [])[0]
    message = change.get("value", {}).get("messages", [])[0]

    message_data = {
        "phoneNumber": message.get("from"),
        "timestamp": message.get("timestamp"),
        "type": message.get("type"),
        "text": None,
        "caption": None,
        "mime_type": None,
        "id": None,
        "filename": None,
    }

    if message_data["type"] == "text":
        message_data["text"] = message.get("text", {}).get("body")
    elif message_data["type"] == "image":
        image = message.get("image", {})
        message_data.update({
            "caption": image.get("caption"),
            "mime_type": image.get("mime_type"),
            "id": image.get("id"),
        })
    elif message_data["type"] == "audio":
        audio = message.get("audio", {})
        audio_mime_type = audio.get("mime_type", "")
        message_data.update({
            "type": audio_mime_type.split(";")[0] if ";" in audio_mime_type else audio_mime_type,
            "id": audio.get("id"),
        })
    elif message_data["type"] == "document":
        document = message.get("document", {})
        message_data.update({
            "filename": document.get("filename"),
            "type": document.get("mime_type"),
            "id": document.get("id"),
        })

    return message_data

