# Interactive CLI Based Ubuntu System Chatbot

An intelligent, AI-powered command-line assistant aimed at simplifying Ubuntu system management. This chatbot behaves like a pair programmer for your terminal—translating natural language requests into actual shell commands, executing them, and then explaining the results in plain English.

## 🚀 Features

*   **Natural Language Command Execution**: Just say "Check my disk usage" or "List all Docker containers," and the bot translates it to the correct shell command (e.g., `df -h` or `docker ps`).
*   **AI-Powered Reasoning**: Before running a command, the AI explains *why* it chose that command.
*   **Intelligent Summaries**: Instead of reading raw terminal output, the bot analyzes the result and gives you a human-readable summary.
*   **Interactive Shell**: Built with `typer` and `rich`, providing a beautiful, colored interface with spinners and status panels.
*   **System Health Checks**: Built-in keywords like `status` or `health` for quick system diagnostics.
*   **Gemini AI Integration**: Uses Google's state-of-the-art Gemini models for high-speed reasoning.

## 🛠️ Prerequisites

*   **Operating System**: Linux (Ubuntu/Debian recommended) or macOS.
*   **Python**: Version 3.10 or higher.
*   **API Key**: A Google Gemini API Key (Get it for free [here](https://aistudio.google.com/app/apikey)).

## 📦 Installation

1.  **Clone the Repository**
    ```bash
    git clone https://github.com/karthik0497/Interactive-CLI-Based-Ubuntu-System-Chatbot.git
    cd Interactive-CLI-Based-Ubuntu-System-Chatbot
    ```

2.  **Install Dependencies**
    ```bash
    pip install -r requirements.txt
    ```

3.  **Set Up Environment (Optional)**
    You can manually create a `.env` file, or the app will ask for your API key on the first run.
    ```bash
    # (Optional)
    echo "GEMINI_API_KEY=your_key_here" > .env
    ```

## 🎮 Usage

Run the main script to start the chatbot:

```bash
python main.py
```

### Example Interaction

```text
You > Check available RAM
AI Reasoning: retrieving memory statistics.
Executing: free -h

AI Summary:
You have a total of 16GB RAM, with 4.2GB currently in use and 11.8GB available.
```

## 📂 Project Structure

*   `main.py`: The entry point for the application. Handles the CLI loop and user input.
*   `modules/ai_engine.py`: Manages interactions with the Google Gemini API (command generation & summarization).
*   `modules/executor.py`: Safely executes shell commands and captures output.
*   `modules/system_checker.py`: Contains utility functions for quick system health metrics.

## 🛡️ Privacy & Security

*   Looking for an API Key? The app requires a Google Gemini API key to function smartly.
*   **Privacy**: Your command history is sent to the AI for processing but is not stored by this application permanently.
*   **Safety**: Always review the commands the AI proposes before confirming execution (future feature). Currently, it runs commands that are deemed safe.

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.
