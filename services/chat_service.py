import os
import uuid

from dotenv import load_dotenv
from openai import OpenAI

from models.chat import ChatManager

load_dotenv()

a4f_api_key = os.getenv("A4F_API_KEY")
a4f_base_url = "https://api.a4f.co/v1"


class ChatService:
    """Service class for managing chat interactions with an AI assistant.
    This class handles chat session creation, message processing, and communication
    with an OpenAI-compatible API. It integrates with a ChatManager to maintain
    conversation history and manages system prompts for AI responses.
    Attributes:
        chat_manager (ChatManager): Manager for handling chat sessions and message storage.
        openai_client (OpenAI): Client for communicating with the OpenAI-compatible API.
        system_prompt (str): The system prompt loaded from file, used to set AI behavior.
    """
    def __init__(self):
        self.chat_manager = ChatManager()
        self.openai_client = OpenAI(base_url=a4f_base_url, api_key=a4f_api_key)
        self.system_prompt = self.load_system_prompt("data/system_prompt.txt")

    def load_system_prompt(self, file_path: str) -> str:
        """Load the system prompt from file."""
        try:
            with open(file_path, "r", encoding="utf-8") as f:
                return f.read()
        except (FileNotFoundError, IOError) as e:
            print(f"Error loading system prompt: {e}")
            return "You are a helpful assistant."

    def create_chat(self, user_id: str) -> str:
        """Create a new chat session."""
        chat_id = str(uuid.uuid4())
        self.chat_manager.create_chat(user_id, chat_id, self.system_prompt)
        return chat_id

    def process_message(self, user_id: str, chat_id: str, message: str) -> str:
        """Process a user message and get AI response."""
        chat = self.chat_manager.get_chat(user_id, chat_id)
        if not chat:
            raise ValueError("Chat not found")

        # Add user message
        self.chat_manager.add_message(user_id, chat_id, "user", message)

        try:
            # Get AI response
            conversation = self.chat_manager.get_conversation(user_id, chat_id)
            # print(f"Sending conversation to API: {conversation}")

            response = self.openai_client.chat.completions.create(
                model="provider-6/gpt-oss-20b",
                messages=conversation,
                temperature=0.7,
                max_tokens=300,
            )

            ai_message = response.choices[0].message.content
            # print(f"AI Response: {ai_message}")

            # Add AI response to chat history
            self.chat_manager.add_message(user_id, chat_id, "assistant", ai_message)

            return ai_message

        except Exception as e:
            print(f"Error in process_message: {str(e)}")
            raise RuntimeError(f"Error getting AI response: {str(e)}") from e
