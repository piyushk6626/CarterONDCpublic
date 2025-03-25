# Directory Structure

Below is a detailed explanation of the Cart-ONDC directory structure:

```
cart_ondc/
├── __init__.py                 # Package initialization, version info
├── api/                        # API endpoints
│   ├── __init__.py             # API package initialization
│   ├── app.py                  # Flask application factory
│   └── webhook.py              # WhatsApp webhook handlers
├── core/                       # Core components
│   ├── __init__.py             # Core package initialization
│   ├── database.py             # SQLite database operations
│   └── firebase.py             # Firebase Firestore operations
├── services/                   # Service layer
│   ├── __init__.py             # Services package initialization
│   ├── download_service.py     # Media download service for WhatsApp
│   ├── messaging.py            # Conversation management service
│   └── whatsapp_service.py     # WhatsApp API integration service
├── registration/               # Registration modules
│   ├── __init__.py             # Registration package initialization
│   ├── base_registration.py    # Abstract base class for registration
│   ├── kiriana_registration.py # Kiriana store registration handler
│   ├── restaurant_registration.py # Restaurant registration handler
│   └── registration_factory.py # Factory pattern for registration handlers
├── store_types/                # Store type definitions
│   ├── __init__.py             # Store types package initialization
│   └── store_type.py           # Store type selection and templates
├── inventory_creation/         # Inventory management
│   └── __init__.py             # Inventory creation package initialization
├── models/                     # Data models
│   └── __init__.py             # Models package initialization
└── utils/                      # Utility functions
    └── __init__.py             # Utilities package initialization
```

## Root Directory

- `__init__.py` - Contains package version and metadata
- `main.py` - Entry point for running the application
- `setup.py` - Package installation script
- `requirements.txt` - List of dependencies
- `UPDATED_README.md` - Project documentation
- `.env` - Environment variables (not tracked in git)
- `auth.json` - Firebase credentials (not tracked in git)

## API Module

The `api` module contains all the HTTP endpoints for the application.

- `__init__.py` - Package initialization
- `app.py` - Flask application factory and configuration
- `webhook.py` - Handles WhatsApp webhook requests

## Core Module

The `core` module contains essential components for the application.

- `__init__.py` - Package initialization
- `database.py` - SQLite database operations for storing registration data
- `firebase.py` - Firebase Firestore operations for storing WhatsApp messages

## Services Module

The `services` module contains service-level components.

- `__init__.py` - Package initialization
- `download_service.py` - Handles downloading media from WhatsApp API
- `messaging.py` - Manages conversations and message flow
- `whatsapp_service.py` - Handles sending and receiving WhatsApp messages

## Registration Module

The `registration` module handles store registration.

- `__init__.py` - Package initialization
- `base_registration.py` - Abstract base class for all registration handlers
- `kiriana_registration.py` - Kiriana store registration handler
- `restaurant_registration.py` - Restaurant registration handler
- `registration_factory.py` - Factory for creating registration handlers

## Store Types Module

The `store_types` module defines different store types and their templates.

- `__init__.py` - Package initialization
- `store_type.py` - Store type selection and templates

## Inventory Creation Module

The `inventory_creation` module handles creating and managing product inventories.

- `__init__.py` - Package initialization

## Models Module

The `models` module contains data models for the application.

- `__init__.py` - Package initialization

## Utils Module

The `utils` module contains utility functions used across the application.

- `__init__.py` - Package initialization 