# PyPilot: Your Personal AI Assistant

PyPilot is a Streamlit-based application that integrates with the Claude AI model from Anthropic. This application allows you to interact with Claude AI in a conversational manner, maintaining context over multiple interactions. It is designed to assist with coding tasks, providing help and managing conversation history for ongoing projects.

## Features

- **Streamlit Interface**: A user-friendly web interface for interacting with Claude AI.
- **Context Management**: Saves and loads conversation context to maintain continuity.
- **Project Management**: Allows you to manage multiple projects with separate conversation histories.
- **Retry Mechanism**: Automatically retries API calls in case of communication errors.

## Prerequisites

- Python 3.7 or higher
- Streamlit
- Anthropic API key

## Installation

Clone the repository:

```bash
git clone https://github.com/Codewithshagbaor/PyPilot
cd PyPilot
```

Install the required packages:

```bash
pip install -r requirements.txt
```

## Usage

Run the Streamlit application:

```bash
streamlit run app.py
```

Open your web browser and navigate to [http://localhost:8501](http://localhost:8501).

1. Enter your Anthropic API key in the sidebar.
2. Enter a project name or use the default project name provided.
3. Start interacting with Claude AI through the chat interface.

## Code Explanation

### ClaudeAI Class

- **Initialization**: Sets up the Claude AI client with the provided API key and defines the number of retry attempts.
- **send_message**: Sends a message to the Claude API and handles retries in case of failures.
- **manage_context**: Manages conversation context by loading previous messages, sending the current message, receiving a reply, and saving the updated context.
- **load_context**: Loads conversation context from a JSON file.
- **save_context**: Saves conversation context to a JSON file.

### Streamlit App

- **main**: Configures the Streamlit app, manages session state, and defines the chat interface.
- **Sidebar**: Allows users to input their API key and manage project names.
- **Chat Interface**: Displays messages and handles user input, sending messages to Claude AI and displaying responses.

## Example

Here’s a simple example of how to interact with the app:

1. Enter your Anthropic API key in the sidebar.
2. Use the default project name or enter a new one.
3. Type a message in the chat input and press Enter.
4. Wait for Claude AI to respond and see the conversation history update.

## Troubleshooting

- **No API Key**: Ensure you enter a valid Anthropic API key in the sidebar.
- **Context Loading Issues**: Check if the JSON files for context are correctly formatted and accessible.
- **API Errors**: Verify your API key and ensure you have an active internet connection.

## Contributing

Feel free to open issues or pull requests if you have suggestions or improvements.

## License

This project is licensed under the MIT License. See the LICENSE file for details.

Enjoy coding with your personal AI assistant! 🎉
