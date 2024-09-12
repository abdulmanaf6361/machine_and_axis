# machine_and_axis

This project provides functionality to manage machines and their respective axes using Django, Redis, and WebSocket for real-time data handling.

## Step 1: Initial Setup

### 1.1 Activate Virtual Environment
Activate the virtual environment:

```bash
# For Windows
.\venv\Scripts\activate

# For Linux/macOS
source venv/bin/activate
```

### 1.2 Install Dependencies
Install all required packages:

```bash
pip install -r requirements.txt
```

### 1.3 Set Up the Database
Run the following commands to set up the database:

```bash
python manage.py makemigrations
python manage.py migrate
```

### 1.4 Create Superuser
Create a superuser:

```bash
python manage.py createsuperuser
```

### 1.5 Start the Django Server
Run the Django development server:

```bash
python manage.py runserver
```

### 1.6 Configure User Groups
1. Access the admin panel at `http://127.0.0.1:8000/admin`.
2. Create 3 user groups:
   - Manager
   - Supervisor
   - Operator

**Note:** A user with `staff=True` is considered as a **SuperAdmin**. Ensure the group names are case-sensitive.

3. Create users and assign them to the respective groups.

## Step 2: Install Redis

Redis is used for:
- **Channel Layers** for WebSocket communication.
- **Message Queue** to handle fast incoming data, avoiding data loss due to database write limitations.

### Installation Instructions:
1. Download Redis from [this link](https://github.com/tporadowski/redis/releases/download/v5.0.14.1/Redis-x64-5.0.14.1.zip).
2. Unzip the file and navigate to the folder via Command Prompt.
3. Start the Redis server:

```bash
redis-server.exe
```

## Step 3: Generate Dummy Data

To create dummy data, run two scripts in parallel:

1. **`script.py`**: Generates a CSV file with dummy data.
2. **`database_script.py` & `redis_script.py`**: Populate Redis and the database with the dummy data.

## Step 4: Test the API

### Install Postman
Use [Postman](https://www.postman.com/) to test the API. Import the Postman collection from [this link](https://www.postman.com/crimson-shuttle-786679/workspace/public-ethereal/collection/32606943-4ed28e87-7c97-4000-8286-2e760ca86e1a?action=share&creator=32606943) or may be [this link](https://elements.getpostman.com/redirect?entityId=32606943-4ed28e87-7c97-4000-8286-2e760ca86e1a&entityType=collection)

### API Testing Steps:
1. First, get the access token by providing the username and password for the user using the "Get Token" API.
2. Copy the access token and paste it into the **Variables** section of Postman.
3. You can now test the various APIs.

## Step 5: WebSocket Client

Use the `websocket.py` script to act as a WebSocket client. This script sends data to the server through a WebSocket connection.

