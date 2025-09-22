# Gemini AI Wrapper REST
<p align="center">
    <img src="https://raw.githubusercontent.com/RahadyanRizqy/gawrestapi/refs/heads/main/assets/gawrestpy.png" width="75%" alt="Gemini Banner" align="center">
</p>
A FastAPI-based wrapper for interacting with Google's Gemini AI. This project provides a simple HTTP API to communicate with Gemini AI, making it easy to integrate AI capabilities into your applications.

## Features

- 🚀 Fast and efficient API server using FastAPI
- 🛠️ Environment variable configuration
- 📊 Built-in logging

## Prerequisites

- Python 3.13 or higher
- A Google account with access to Gemini
- Required cookies for authentication

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/RahadyanRizqy/gawrestapi.git
   cd gawrestapi
   ```

2. Create and activate a virtual environment (recommended):
   ```bash
   python -m venv .venv
   .venv\Scripts\activate  # On Windows
   # or
   source .venv/bin/activate  # On Unix or MacOS
   ```

3. Install the required dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Configuration

1. Copy the `.env.example` file to `.env`:
   ```bash
   cp .env.example .env
   ```

2. Edit the `.env` file with your configuration:
   ```env
   PORT=5800
   SECRET_KEY=your_secret_key_here
   LOG_LEVEL=INFO
   ```

   Alternatively, you can create a `cookies.txt` file with your cookie header.

## Obtaining Cookies

1. Log in to [Gemini](https://gemini.google.com/) in your browser
2. Use Cookie-Editor extension and copy the header-string
3. Paste it into `cookies.txt`

## Running the Application

Start the server:
```bash
uvicorn main:app --reload --port 5800
```

The API will be available at `http://localhost:5800`

## API Documentation

### Authentication
All endpoints except `/` require authentication. Include the JWT token in the `Authorization` header:
```
Authorization: Bearer your_jwt_token_here
```

### Endpoints

#### 1. Root Endpoint
- **URL**: `GET /`
- **Description**: Health check endpoint to verify the API is running
- **Response**: 
  ```json
  {
    "status": "ok",
    "message": "API is running"
  }
  ```

#### 2. Chat with Gemini
- **URL**: `POST /chat`
- **Description**: Send a message to Gemini AI
- **Headers**:
  - `Content-Type: application/json` or `multipart/form-data` (for files only)
  - `X-Chat-Metadata`: (Optional) Simplified chat metadata for continuing conversations
- **Request Body (JSON)**:
  ```json
  {
    "message": "Your message to Gemini"
  }
  ```
- **Request Body (Form Data)**:
  - `message`: (string) Your message to Gemini
  - `files`: (file, optional) One or more files to include with the message
- **Response**:
  ```json
  {
    "data": {
      "text": "Gemini's response",
      "is_new_chat": true,
      "user": "user_id"
    }
  }
  ```
- **Response Headers**:
  - `X-Chat-Metadata`: Simplified metadata to continue this conversation

#### 3. Chat with Specific Gemini Model
- **URL**: `POST /chat/{gem_id}`
- **Description**: Send a message to a specific Gemini model
- **Path Parameters**:
  - `gem_id`: (string) ID of the specific Gemini model to use
- **Request/Response**: Same as the `/chat` endpoint

#### 4. List Available Gemini Models
- **URL**: `GET /gems`
- **Description**: Get a list of available Gemini models
- **Query Parameters**:
  - `predefined`: (boolean, optional) Filter by predefined models
  - `hidden`: (boolean, optional) Include hidden models
- **Response**:
  ```json
  {
    "data": {
      "gems": [
        {
          "id": "gemini-pro",
          "name": "Gemini Pro",
          "description": "General purpose model",
          "predefined": true
        }
      ],
      "user": "your_details"
    }
  }
  ```

#### 5. Get Specific Gemini Model
- **URL**: `GET /gems/{gem_id}`
- **Description**: Get details about a specific Gemini model
- **Path Parameters**:
  - `gem_id`: (string) ID of the Gemini model
- **Response**: Same as list endpoint but for a single model

#### 6. Create Custom Gemini Model
- **URL**: `POST /gems`
- **Description**: Create a custom Gemini model
- **Request Body**:
  ```json
  {
    "name": "My Custom Model",
    "prompt": "You are a helpful assistant",
    "description": "My custom model description"
  }
  ```
- **Response**:
  ```json
  {
    "data": {
      "id": "custom-model-123",
      "name": "My Custom Model",
      "prompt": "You are a helpful assistant",
      "description": "My custom model description"
    }
  }
  ```

#### 7. Update Gemini Model
- **URL**: `PUT /gems/{gem_id}`
- **Description**: Update a Gemini model's properties
- **Path Parameters**:
  - `gem_id`: (string) ID of the Gemini model to update
- **Request Body**: (any of these fields can be included)
  ```json
  {
    "name": "Updated Name",
    "prompt": "Updated prompt",
    "description": "Updated description"
  }
  ```

#### 8. Delete Gemini Model
- **URL**: `DELETE /gems/{gem_id}`
- **Description**: Delete a custom Gemini model
- **Path Parameters**:
  - `gem_id`: (string) ID of the Gemini model to delete

## Project Structure

```
.
├── .env.example          # Example environment variables
├── .gitignore           # Git ignore file
├── main.py              # Main application entry point
├── requirements.txt     # Python dependencies
├── handlers/            # Request handlers
├── middleware/          # Custom middleware
├── utils/               # Utility functions
└── web/                 # Web routes and API endpoints
```

## Environment Variables

| Variable       | Default   | Description                              |
|----------------|-----------|------------------------------------------|
| PORT           | 5800      | Port to run the server on                |
| SECRET_KEY     | changeme  | Secret key for the application           |
| LOG_LEVEL     | INFO      | Logging level (DEBUG, INFO, WARNING, etc.) |

## Disclaimer

This project is not affiliated with or endorsed by Google. Use at your own risk. Make sure to comply with Google's Terms of Service when using this software.
