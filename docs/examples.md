# Cart-ONDC Usage Examples

This document provides examples of how to use the Cart-ONDC package for different scenarios.

## Basic Setup

```python
# Import the Flask application
from cart_ondc.api.app import app

# Run the application
if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)
```

## WhatsApp Service Usage

```python
from cart_ondc.services.whatsapp_service import whatsapp_service

# Send a message to a WhatsApp user
whatsapp_service.send_message("Hello, welcome to Cart-ONDC!", "1234567890")

# Receive and process a text message
message = whatsapp_service.receive_message("1234567890")
print(f"Received message: {message}")

# Receive and download an image
image_path = whatsapp_service.receive_image("1234567890")
if image_path:
    print(f"Image downloaded to: {image_path}")
```

## Registration Process

```python
from cart_ondc.registration.registration_factory import RegistrationFactory

# Create a registration handler for a specific store type
registration = RegistrationFactory.create_registration("kiriana", "1234567890")

# Start the registration process
result = registration.register()

if result:
    print("Registration completed successfully!")
else:
    print("Registration was interrupted or failed.")
```

## Conversation Management

```python
from cart_ondc.services.messaging import conversation_manager

# Start a new conversation
conversation_manager.start_conversation("1234567890")

# Update the conversation state
conversation_manager.update_conversation(
    "1234567890",
    state="registration",
    progress=2,
    data={"store_type": "kiriana"}
)

# Get the current conversation state
state = conversation_manager.get_conversation_state("1234567890")
print(f"Current state: {state}")

# Prompt for information
reply = conversation_manager.prompt_for_info(
    "1234567890",
    "business_name",
    "Please enter your business name:"
)
print(f"User replied: {reply}")
```

## Firebase Operations

```python
from cart_ondc.core.firebase import firebase_client

# Store a WhatsApp message
message_id = firebase_client.add_whatsapp_message(webhook_data)
print(f"Message stored with ID: {message_id}")

# Get the latest message from a user
latest_message = firebase_client.get_latest_message("1234567890")
print(f"Latest message: {latest_message}")
```

## Database Operations

```python
from cart_ondc.core.database import db_manager

# Store registration data
data = {
    "name": "John Doe",
    "dob": "01/01/1990",
    "pancard": "ABCDE1234F",
    "gst_number": "22AAAAA0000A1Z5",
    "address": "123 Main St",
    "business_name": "John's Grocery",
    "trade_license": "TL123456",
    "udyam": "UDYAM-AB-01-0000000",
    "account_number": "1234567890",
    "ifsc_code": "ABCD0123456",
    "upi_id": "johndoe@bankname",
    "phoneNumber": "1234567890"
}

result = db_manager.store_kiriana_data(data)
if result:
    print("Data stored successfully!")

# Check if a user is verified
is_verified = db_manager.is_verified("1234567890")
print(f"Is verified: {is_verified}")

# Set a user as verified
db_manager.set_verified("1234567890", True, "kiriana")
```

## Store Type Management

```python
from cart_ondc.store_types.store_type import store_type_manager

# Get the store type selection message
message = store_type_manager.select_store_type()
print(message)

# Get the registration flow for a specific store type
registration_flow = store_type_manager.get_registration_flow("kiriana")

# Iterate through the registration flow
for prompt in registration_flow:
    print(prompt)
``` 