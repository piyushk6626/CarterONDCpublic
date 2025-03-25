# Cart-ONDC

Cart-ONDC is a WhatsApp-based solution for onboarding sellers to the Open Network for Digital Commerce (ONDC) in India.

## Overview

This application enables sellers, even those who are not tech-savvy, to easily onboard to the ONDC network and create digital inventories. The system leverages WhatsApp as a familiar interface for sellers, supports natural language conversations, and provides a streamlined registration process.

## Features

- **WhatsApp Integration**: Use WhatsApp Business API to communicate with sellers
- **Multi-store Support**: Register different types of stores, including:
  - Kiriana Stores (Grocery & Packaged Food)
  - Clothing Stores
  - Handicraft Shops
  - Restaurants / Sweet & Snack Shops
- **Automated Registration**: Guide sellers through the registration process step-by-step
- **Document Management**: Collect and verify required documents like GST, PAN, FSSAI, etc.
- **AI-powered Inventory Management**: Assist in creating digital inventories

## Project Structure

```
cart_ondc/
├── __init__.py                 # Package initialization
├── api/                        # API endpoints
│   ├── __init__.py
│   ├── app.py                  # Flask app configuration
│   └── webhook.py              # WhatsApp webhook handlers
├── core/                       # Core components
│   ├── __init__.py
│   ├── database.py             # SQLite database operations
│   └── firebase.py             # Firebase operations
├── services/                   # Service layer
│   ├── __init__.py
│   ├── download_service.py     # Media download service
│   ├── messaging.py            # Conversation management
│   └── whatsapp_service.py     # WhatsApp API integration
├── registration/               # Registration modules
│   ├── __init__.py
│   ├── base_registration.py    # Base registration class
│   ├── kiriana_registration.py # Kiriana store registration
│   ├── restaurant_registration.py # Restaurant registration
│   └── registration_factory.py # Factory for creating registration handlers
├── store_types/                # Store type definitions
│   ├── __init__.py
│   └── store_type.py           # Store type selection and templates
├── inventory_creation/         # Inventory management
│   └── __init__.py
├── models/                     # Data models
│   └── __init__.py
└── utils/                      # Utility functions
    └── __init__.py
```

## Technical Stack

- **Backend**: Python, Flask
- **Database**: SQLite (local data), Firestore (message storage)
- **External Services**: WhatsApp Business API
- **Authentication**: Firebase Admin SDK

## Installation and Setup

1. Clone the repository:
   ```
   git clone <repository-url>
   cd cart-ondc
   ```

2. Create a virtual environment:
   ```
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install dependencies:
   ```
   pip install -r requirements.txt
   ```

4. Create a `.env` file with the following variables:
   ```
   PHONE_ID=your_whatsapp_phone_id
   ACCESS_TOKEN=your_whatsapp_access_token
   ```

5. Place your Firebase Admin SDK credentials in `auth.json`

6. Run the application:
   ```
   python main.py
   ```

## Usage

### Registering a Store

1. The seller interacts with the WhatsApp number.
2. The system sends a welcome message with store type options.
3. The seller selects their store type.
4. The system guides the seller through the registration process, collecting required information.
5. Upon completion, the seller's information is stored and submitted for verification.

### Verification Process

1. The system stores the seller's information in the SQLite database.
2. The information is marked as pending verification.
3. Once verified (manually or automatically), the seller can proceed to create their inventory.

## Configuration

- **WhatsApp API**: Configure your WhatsApp Business API credentials in the `.env` file.
- **Firebase**: Place your Firebase Admin SDK service account JSON file as `auth.json` in the project root.
- **Database**: By default, the application uses SQLite. The database file is created as `database.db` in the project root.

## Development

### Adding New Store Types

1. Create a new registration module in the `registration` package, extending `BaseRegistration`.
2. Implement the required methods: `store_type`, `required_fields`, and `store_data`.
3. Add the necessary database functions in `database.py`.
4. Add the store type to the `RegistrationFactory` in `registration_factory.py`.
5. Add the registration flow in `store_type.py`.

### Extending the API

1. Create a new blueprint in the `api` package.
2. Implement your routes and handlers.
3. Register the blueprint in `app.py`.

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgements

- Open Network for Digital Commerce (ONDC) for providing the framework for digital commerce in India.
- WhatsApp Business API for enabling business-customer communications. 