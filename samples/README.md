# Ollama Chat Application

A simple chat application that connects to a local Ollama instance and uses the llama3.1 model for conversations.

## Requirements

- **Ollama**: Running locally on `localhost:11434`
- **Python**: 3.8 or higher
- **Dependencies**: requests (will be installed automatically)

## Installation

1. **Install Ollama** (if not already installed):
   - Visit [ollama.ai](https://ollama.ai) and follow installation instructions for your OS

2. **Install the llama3.1 model**:
   ```bash
   ollama pull llama3.1
   ```

3. **Start Ollama server**:
   ```bash
   ollama serve
   ```
   (The server will run on `localhost:11434`)

4. **Install Python dependencies**:
   ```bash
   pip install -e .
   ```
   or
   ```bash
   pip install requests
   ```

## Usage

Run the chat application:

```bash
python samplechat.py
```

### Commands

- Type your message and press Enter to chat
- `clear` - Clear the conversation history
- `history` - Show the full conversation history
- `quit` or `exit` - Exit the application

### Example Session

```
You: What is Python?
llama3.1: Python is a high-level, interpreted programming language...

You: Can you explain decorators?
llama3.1: Decorators in Python are functions that modify other functions...

You: clear
✓ Conversation history cleared

You: quit
Goodbye!
```

## Features

- **Streaming responses**: Responses are displayed in real-time as the model generates them
- **Conversation history**: The application maintains context across messages
- **Error handling**: Graceful handling of connection issues and timeouts
- **Simple interface**: Clean command-line chat interface

## Notes

- The first request may take a moment as the model is loaded into memory
- Ensure Ollama is running before starting the chat application
- The application maintains conversation context for more coherent responses
