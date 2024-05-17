# AI Agents Talking

Welcome to the **AI Agents Talking** repository! This project enables interactive conversations between AI agents with memory management using the Groq API. The app is built with Streamlit and features a dynamic, persistent memory to enhance the contextual relevance of conversations. Users can also generate detailed summaries of the conversations.

## Features

- **Interactive AI Conversations**: Start and observe conversations between AI agents.
- **Memory Management**: Persistent shared memory across interactions, ensuring contextual continuity.
- **Dynamic Weights**: Tracks word frequency to highlight important thoughts.
- **Detailed Summaries**: Generates structured, insightful summaries of the conversation history.

## Installation

To get started, clone the repository and install the required packages.

```bash
git clone https://github.com/yourusername/AI-agents-talking.git
cd AI-agents-talking
pip install -r requirements.txt
```

## Usage

To run the Streamlit app, use the following command:

```bash
streamlit run main.py
```

### Step-by-Step Guide

1. **API Key Setup**: Enter your Groq API key in the sidebar.
2. **Add Thought**: Input a thought to initialize the shared memory.
3. **Start Conversation**: Configure the number of conversation turns and observe the interaction between the AI agents.
4. **View Summary**: After the conversation, view a detailed summary of the entire interaction.

## Code Overview

### interactive_ai.py

The main script for the Streamlit app. It includes the following key functions:

- **manage_memory**: Manages the size of shared memory.
- **get_weighted_context**: Retrieves a weighted context from the shared memory.
- **interact_with_groq**: Interacts with the Groq API to get AI responses.
- **generate_summary**: Generates a summary of the conversation.

## Contributing

Contributions are welcome! Please open an issue or submit a pull request for any improvements or new features.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

## Acknowledgments

- Thanks to the developers of [Streamlit](https://streamlit.io/) for creating an easy-to-use framework for building interactive web apps.
- Special thanks to [Groq](https://groq.com/) for providing the AI capabilities that power this app.
