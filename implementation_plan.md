# Implementation Plan: Interactive CLI-Based Ubuntu System Chatbot

## Goal
Build a Linux-based interactive CLI chatbot that can:
1.  Check system status (CPU, Memory, Disk, etc.).
2.  Take natural language user requests.
3.  Suggest commands to fix issues or perform tasks.
4.  Execute commands **only** after user permission.
5.  Explain usage.

## Architecture

### Tech Stack
-   **Language**: Python 3.10+
-   **CLI Framework**: `typer` or standard `argparse` with a `while` loop.
-   **UI Library**: `rich` (for beautiful tables, colors, and prompts).
-   **System Info**: `psutil` (for cross-platform system monitoring).
-   **AI/LLM Integration**:
    -   Since "Antigravity" (the coding assistant) does not have a runtime API for apps, we will design the app to use a standard Provider (like Google Gemini or OpenAI) or a local model (Ollama) if preferred.
    -   *Note*: For the initial prototype, we can mock the AI part or ask the user for an API Key.

### Modules

1.  **`main.py`**: The entry point. Handles the main event loop (repl).
2.  **`modules/system_checker.py`**: Functions to fetch CPU, RAM, and Disk usage.
3.  **`modules/executor.py`**: A safe wrapper around `subprocess` that asks for confirmation.
4.  **`modules/ai_engine.py`**: (Future) Connects to an LLM to generate Bash commands from English text.

## Development Steps

1.  **Setup**: Create project structure and virtual environment.
2.  **System Stats**: Implement `system_checker` to show a dashboard.
3.  **Executor**: Implement the "Ask for Permission" logic.
4.  **Chat Interface**: Build the REPL (Read-Eval-Print Loop) where users type requests.
5.  **Integration**: Connect the pieces.

## Concerning "Antigravity Developer API"
"Antigravity" is the AI Agent assisting you right now. I do not provide a runtime API for your Python application to call. To make the chatbot "smart" (i.e., understanding "fix my wifi" -> `sudo systemctl restart NetworkManager`), we need to integrate a third-party LLM API (like Google Gemini, OpenAI, or a local model).
