# My Inventory Backend

## Overview
This is the backend for the My Inventory system. It is a RESTful API that provides endpoints for managing the following:
- User Authentication
- Inventory Management
- Transactions and Purchases
- File Uploads for Bulk Inventory Addition

## Getting Started
### Prerequisites
- Pipenv or pip

### Installation Instructions
- Clone the repository

### Setup and Configuration
- Run ``` python manage.py migrate ``` to apply the migrations.
- Create a superuser using ``` python manage.py createsuperuser ```.
- Run the server using ``` python manage.py runserver ```.

## Architecture

### Project Structure

The project follows a standard Django structure with some customizations. Below is an overview of the key directories and files:

#### Root Directory
- **`manage.py`**: Command-line utility for administrative tasks (e.g., running the server, creating migrations).
- **`requirements.txt`**: Lists the Python packages required for the project.
- **`Pipfile`**: Contains the Python packages required for the project.
- **`README.md`**: Documentation file that provides an overview of the project.

#### `backend/`
- **`settings.py`**: Contains project settings and configurations.
- **`urls.py`**: Contains the endpoint URLs for the project.
- **`wsgi.py`**: WSGI entry point for the application.
- **`asgi.py`**: ASGI entry point for asynchronous capabilities.

#### `api/`
- **`__init__.py`**: Marks this directory as a Python package.
- **`models.py`**: Contains the database models for the application.
- **`views.py`**: Defines the views (business logic) for the application.
- **`serializers.py`**: Contains serializers for converting complex data types into JSON and vice versa 
- **`forms.py`**: Contains a form for handling file uploads.
- **`tests/`**: Contains test cases for the application.
  - **`__init__.py`**: Marks this directory as a Python package.
  - **`test_views.py`**: Contains tests for the views.

#### `migrations/`
- **`__init__.py`**: Marks this directory as a Python package.
- Contains migration files for database schema changes.

## Models
Here is an overview of the key models and their relationships:

### Custom User Model
The project uses a **custom user** model instead of Django’s built-in user model. The Custom User Model extends Django’s AbstractUser to create a user model with additional fields and a custom manager.

**Fields:**
- `email`: The user's email address.
- `password`: The user's password.
- `first_name`: The user's first name.
- `last_name`: The user's last name.
- `is_staff`: Indicates if the user is staff.
- `is_superuser`: Indicates if the user is a superuser.

**Custom Manager**: Handles user creation and superuser creation with custom validations. It overrides the `create_user` and `create_superuser` methods to ensure the email is normalized and required fields are provided.

### Inventory Model
The Inventory Model represents an inventory item in the system.

**Fields:**
- `name`: The name of the inventory item.
- `description`: A text field providing details about the item.
- `price`: The price of the inventory item.
- `quantity`: The quantity available in stock.

### Transaction Model
The Transaction Model logs each transaction, recording details about the purchased items.

**Fields:**
- `item`: A foreign key field referencing the inventory item being purchased.
- `quantity`: The quantity of the item purchased.
- `date`: The date of the transaction.

**Relationships:**
Each transaction is associated with one inventory item.

## APIs

### Endpoints
1. #### User Endpoints
- **/register/**: Register a new user.
- **/login/**: Authenticate a user and provide a login token.

2. #### Inventory Endpoints
- **inventory/add/**: Add a new inventory item to the system.
- **inventory/**: Retrieve a list of all inventory items.
- **inventory/id/add/**: Update an inventory item by its ID.
- **inventory/id/delete/**: Delete an inventory item by its ID.
- **upload/**: Allows to bulk upload an products using a spreadsheet
3. #### Transaction Endpoints
- **/transactions/**: Retrieve a list of all transactions.

### Serializers
- **UserSerializer**: Serializes User model instances for creating and updating users, and also for reading user data.
- **InventorySerializer**: Serializes Inventory model instances for creating and updating inventory items, and also for reading item data.
- **TransactionSerializer**: Serializes Transaction model instances for creating and updating transactions, and also for reading transaction data.

### Views
#### User Views
- **UserRegistrationView**: Handles user registration by validating and saving user data. No authentication required.
- **UserLoginView**: Authenticates users and returns a token. No authentication required for login.
- **UserDetailView**: Returns details of the currently authenticated user. Requires the user to be authenticated.
- **ChangePasswordView**: Allows authenticated users to update their password. Requires the user to be authenticated.

#### Inventory Views
- **InventoryAddView**: Allows authenticated users to add new inventory items. Requires the user to be authenticated.
- **InventoryListView**: Retrieves a list of all inventory items. No authentication required.
- **InventoryUpdateView**: Allows authenticated users to update an inventory item by its ID. Requires the user to be authenticated.
- **InventoryDeleteView**: Allows authenticated users to delete an inventory item by its ID. Requires the user to be authenticated.

#### Transaction Views
- **TransactionListView**: Retrieves a list of all transactions. No authentication required.

## Testing
To run tests, execute:
```bash
python manage.py test inventory.tests
