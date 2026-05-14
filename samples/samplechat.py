#!/usr/bin/env python3
"""
Simple Chat Application with Ollama llama3.1 Model
Connects to local Ollama instance and maintains conversation history.
"""

import json
import requests
import sys
from typing import Optional
from dotenv import load_dotenv
import os

load_dotenv()



# Configuration
OLLAMA_URL = os.getenv("OLLAMA_URL", "http://localhost:11434")  # Default to localhost if not set
MODEL_NAME = os.getenv("MODEL_NAME", "llama3.1")
TIMEOUT = int(os.getenv("TIMEOUT", 120))  # seconds


class OllamaChatClient:
    """Simple client to interact with Ollama's llama3.1 model."""
    
    def __init__(self, url: str = OLLAMA_URL, model: str = MODEL_NAME):
        """
        Initialize the Ollama chat client.
        
        Args:
            url: Ollama server URL
            model: Model name to use
        """
        self.url = url
        self.model = model
        self.conversation_history = []
    
    def check_server(self) -> bool:
        """Check if Ollama server is running."""
        try:
            response = requests.get(f"{self.url}/api/tags", timeout=5)
            return response.status_code == 200
        except requests.exceptions.ConnectionError:
            return False
    
    def check_model_exists(self) -> bool:
        """Check if the specified model is available."""
        try:
            response = requests.get(f"{self.url}/api/tags", timeout=5)
            if response.status_code == 200:
                models = response.json().get("models", [])
                model_names = [m["name"] for m in models]
                return any(self.model in name for name in model_names)
        except Exception:
            pass
        return False
    
    def send_message(self, user_message: str, stream: bool = True) -> str:
        """
        Send a message to the model and get a response.
        
        Args:
            user_message: The user's message
            stream: Whether to stream the response
            
        Returns:
            The model's response
        """
        # Add user message to history

        self.conversation_history.clear()  # Clear history for stateless interaction

        self.conversation_history.append({
            "role": "user",
            "content": user_message
        })
        
        try:
            response = requests.post(
                f"{self.url}/api/chat",
                json={
                    "model": self.model,
                    "messages": self.conversation_history,
                    "stream": stream,
                },
                timeout=TIMEOUT,
            )
            
            if response.status_code != 200:
                return f"Error: Server returned status code {response.status_code}"
            
            # Parse response
            if stream:
                full_response = ""
                for line in response.iter_lines():
                    if line:
                        try:
                            chunk = json.loads(line)
                            if "message" in chunk:
                                content = chunk["message"].get("content", "")
                                full_response += content
                                # Print chunks in real-time for better UX
                                print(content, end="", flush=True)
                        except json.JSONDecodeError:
                            pass
                print()  # New line after streaming
            else:
                data = response.json()
                full_response = data.get("message", {}).get("content", "")
            
            # Add assistant response to history
            self.conversation_history.append({
                "role": "assistant",
                "content": full_response
            })
            
            return full_response
            
        except requests.exceptions.Timeout:
            return "Error: Request timeout. The model might be processing a large request."
        except requests.exceptions.ConnectionError:
            return "Error: Cannot connect to Ollama server. Is it running on localhost:11434?"
        except Exception as e:
            return f"Error: {str(e)}"
    
    def clear_history(self):
        """Clear the conversation history."""
        self.conversation_history = []
    
    def get_history(self) -> list:
        """Get the current conversation history."""
        return self.conversation_history


def print_welcome():
    """Print welcome message and instructions."""
    print("\n" + "="*60)
    print("Ollama Chat Application - llama3.1")
    print("="*60)
    print("\nCommands:")
    print("  'quit' or 'exit'  - Exit the application")
    print("  'clear'           - Clear conversation history")
    print("  'history'         - Show conversation history")
    print("\nType your message and press Enter to chat.")
    print("-"*60 + "\n")


def main():
    """Main chat application loop."""
    client = OllamaChatClient()
    
    # Check if Ollama server is running
    print("Checking Ollama server...")
    if not client.check_server():
        print("❌ Error: Cannot connect to Ollama server at", OLLAMA_URL)
        print("Make sure Ollama is running. Start it with: ollama serve")
        sys.exit(1)
    
    print("✓ Connected to Ollama server")
    
    # Check if model exists
    print(f"Checking for {MODEL_NAME} model...")
    if not client.check_model_exists():
        print(f"❌ Error: Model '{MODEL_NAME}' not found")
        print(f"Pull it with: ollama pull {MODEL_NAME}")
        sys.exit(1)
    
    print(f"✓ Model '{MODEL_NAME}' is available\n")
    
    print_welcome()
    
    try:
        while True:
            try:
                # Get user input
                user_input = input("You: ").strip()
                
                if not user_input:
                    continue
                
                # Handle commands
                if user_input.lower() in ("quit", "exit"):
                    print("\nGoodbye!")
                    break
                
                if user_input.lower() == "clear":
                    client.clear_history()
                    print("✓ Conversation history cleared\n")
                    continue
                
                if user_input.lower() == "history":
                    print("\n" + "="*60)
                    print("Conversation History:")
                    print("="*60)
                    if not client.conversation_history:
                        print("(empty)")
                    else:
                        for msg in client.conversation_history:
                            role = msg["role"].upper()
                            content = msg["content"]
                            print(f"\n{role}:")
                            print(content)
                    print("\n" + "="*60 + "\n")
                    continue
                
                # Send message to model
                print(f"\n{MODEL_NAME}: ", end="")
                client.send_message(user_input, stream=True)
                print()  # Extra line for readability
                
            except KeyboardInterrupt:
                print("\n\nInterrupted by user")
                break
    
    except EOFError:
        print("\n\nEnd of input reached")
    
    print("\nChat application closed.")


if __name__ == "__main__":
    main()

