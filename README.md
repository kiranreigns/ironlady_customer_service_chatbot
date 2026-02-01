# IronLady Customer Chatbot

A FastAPI-based customer chatbot application that uses OpenAI-compatible APIs to provide intelligent conversational responses.

## Overview

This project is a web-based chatbot interface built with:
- **Backend**: FastAPI with Uvicorn ASGI server
- **Frontend**: HTML with Jinja2 templating and CSS styling
- **AI Model**: OpenAI-compatible API (supports both OpenAI API directly and third-party providers)
- **Session Management**: Starlette sessions for user state management

## Project Structure

```
.
├── main.py                          # FastAPI application entry point
├── check_models.py                  # Model checking utility
├── pyproject.toml                   # Project dependencies and configuration
├── controllers/
│   └── chat_controller.py          # Chat request handlers
├── models/
│   └── chat.py                     # ChatManager for conversation history
├── services/
│   └── chat_service.py             # Chat service with OpenAI integration
├── data/
│   └── system_prompt.txt           # System prompt for AI behavior
├── templates/
│   └── index.html                  # Web interface
└── static/
    └── styles.css                  # Styling
```

## Prerequisites

- Python 3.13 or higher
- pip or [uv](https://docs.astral.sh/uv/) (for faster package management)
- AI API credentials (choose one option):
  - **OpenAI API**: Get your API key from [OpenAI](https://platform.openai.com/api-keys)
  - **Third-party provider** (e.g., A4F): Get API credentials from your provider

## Installation

### Step 1: Clone/Download the Project

Navigate to your project directory:
```bash
cd d:\ironlady tasks\ironlady_customer_chatbot
```

### Step 2: Set Up Environment Variables

Create a `.env` file in the project root directory with your API credentials.

#### Option A: Using OpenAI API Directly (Recommended)
```env
OPENAI_API_KEY=your_openai_api_key_here
OPENAI_MODEL=gpt-3.5-turbo
```

Available OpenAI models:
- `gpt-4` (most capable, higher cost)
- `gpt-4-turbo-preview`
- `gpt-3.5-turbo` (faster, lower cost - default)
- `gpt-3.5-turbo-16k` (extended context)

#### Option B: Using Third-Party Provider (e.g., A4F)
```env
A4F_API_KEY=your_a4f_api_key_here
A4F_BASE_URL=https://api.a4f.co/v1
A4F_MODEL=provider-6/gpt-oss-20b
```

**Note**: You only need to configure ONE option. The application will use whichever API key is available (OpenAI is prioritized if both are set).

### Step 3: Install Dependencies

#### Option A: Using `uv` (Recommended - No Virtual Environment Setup Needed)
```bash
uv sync
```

`uv` automatically creates and manages a virtual environment for you, so no additional setup is required.

#### Option B: Using `pip` (Requires Manual Virtual Environment)

Create a virtual environment first:
```bash
python -m venv venv
```

Activate the virtual environment:
- **Windows**: `venv\Scripts\activate`
- **Mac/Linux**: `source venv/bin/activate`

Then install dependencies:
```bash
pip install -e .
```

Or install dependencies directly:
```bash
pip install fastapi uvicorn openai python-dotenv jinja2 itsdangerous black isort
```

## Running the Application

### Start the Server

Run the application using uv:

```bash
uv run main.py
```

The server will start on `http://localhost:3000`

### Access the Chatbot

Open your web browser and navigate to:
```
http://localhost:3000
```

#### Alternative: Using Uvicorn Directly

If you prefer to run Uvicorn without uv:
```bash
uvicorn main:app --host 0.0.0.0 --port 3000 --reload
```

## API Endpoints

### GET `/`
Returns the main chatbot interface (HTML page).

### POST `/api/create_chat`
Creates a new chat session for the user.
- **Response**: New chat session ID

### POST `/api/send_message`
Sends a message and receives a response from the AI assistant.
- **Request Body**: 
  ```json
  {
    "message": "Your message here",
    "chat_id": "chat_session_id"
  }
  ```
- **Response**: AI assistant's response

## Configuration

### Main Application Settings

In `main.py`:
- **Host**: `0.0.0.0` (accessible from any network interface)
- **Port**: `3000` (change if needed)
- **Reload**: `True` (enables hot-reload during development; disable in production)
- **Secret Key**: Change `"your_secret_key_here"` to a secure random value in production

### AI Model Configuration

In `services/chat_service.py`:
- **OpenAI API**: Uses official OpenAI endpoint with your API key
- **Third-party Provider**: Uses custom base URL (e.g., `https://api.a4f.co/v1`) with provider API key

The application automatically detects which API to use based on environment variables:
1. If `OPENAI_API_KEY` is set, it will use OpenAI API directly
2. If only `A4F_API_KEY` is set, it will use the third-party provider
3. If neither is set, the application will raise an error at startup

### System Prompt

The AI assistant's behavior is controlled by the system prompt located in `data/system_prompt.txt`. Modify this file to customize the chatbot's personality and responses.

## Project Architecture

### Controllers (`controllers/chat_controller.py`)
Handles HTTP requests and manages session data. Routes requests to the appropriate services.

### Services (`services/chat_service.py`)
Contains business logic for:
- Loading system prompts
- Creating chat sessions
- Sending messages to the OpenAI-compatible API
- Managing conversation history

### Models (`models/chat.py`)
Manages chat session data and conversation history storage.

### Templates (`templates/index.html`)
HTML interface for the chatbot with JavaScript for API communication.

## Development

### Code Formatting

Format code with Black:
```bash
black .
```

Sort imports with isort:
```bash
isort .
```

### Check Models

Verify model configuration:
```bash
python check_models.py
```

## Troubleshooting

### API Key Issues
- Ensure `.env` file exists in the project root
- For OpenAI: Get your key from [OpenAI API Keys](https://platform.openai.com/api-keys)
- For third-party providers: Verify the API key and base URL are correctly set
- At least one API option must be configured (OpenAI or third-party provider)
- Check that the API key has the necessary permissions
- If switching API providers, make sure to update the corresponding environment variables

### Port Already in Use
Change the port in `main.py`:
```python
uvicorn.run("main:app", host="0.0.0.0", port=3001, reload=True)
```

### Module Import Errors
- Ensure all dependencies are installed: `uv sync` or `pip install -e .`
- Verify Python version is 3.13+: `python --version`

### Template/Static Files Not Found
- Ensure the `templates/` and `static/` directories exist
- Verify the `index.html` and `styles.css` files are in their respective directories

## Production Deployment

For production use:

1. Set `reload=False` in the Uvicorn configuration
2. Change the session middleware secret key to a secure random value
3. Use environment variables for all sensitive configuration
4. Consider using a production ASGI server (Gunicorn with Uvicorn workers, etc.)
5. Enable HTTPS/SSL
6. Set up proper logging and monitoring

Example production command:
```bash
uvicorn main:app --host 0.0.0.0 --port 3000 --workers 4
```


