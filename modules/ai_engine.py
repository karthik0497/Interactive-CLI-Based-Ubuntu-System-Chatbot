import google.generativeai as genai
import os
import time
from rich.console import Console

console = Console()

class AIEngine:
    def __init__(self):
        self.api_key = os.getenv("GEMINI_API_KEY")
        if not self.api_key:
            return
        
        genai.configure(api_key=self.api_key)
        
        # Priority list of models to try blindly (saves API quota vs list_models)
        # We saw you have 2.5 flash, so we put it first.
        known_models = ['gemini-2.5-flash', 'gemini-1.5-flash', 'gemini-pro']
        model_name = known_models[0]

        # We construct the model. This doesn't hit the API yet.
        self.model = genai.GenerativeModel(model_name)
        self.chat = self.model.start_chat(history=[])
        
        # System Prompt to define behavior
        self.system_instruction = """
        You are an advanced Ubuntu System Assistant running in a CLI.
        Your goal is to help the user manage their system, check status, and execute commands.
        
        PROTOCOL:
        1. When the user asks a question, determine if you need to run a shell command to get the answer.
        2. If YES (Command needed):
           - Respond EXACTLY in this format:
             COMMAND: <actual bash command>
             EXPLANATION: <short reason why>
           - Example:
             User: "Show me my IP address"
             You:
             COMMAND: ip a
             EXPLANATION: retrieving network interface details.

        3. HANDLING FILE EDITS & CRON JOBS (CRITICAL):
           - DO NOT suggest interactive editors like 'nano', 'vim', 'vi', 'gedit', or 'crontab -e'.
           - Instead, generate commands that perform the edit non-interactively.
           - For Crontab:
             Use: (crontab -l 2>/dev/null; echo "your_cron_line") | crontab -
           - For Appending to files:
             Use: echo "content" >> filename
           - For Overwriting/Creating files:
             Use: echo "content" > filename
           - The user wants YOU to do the work, not open an editor for them.
        
        4. If NO (General chat or explanation):
           - Just answer normally.
        
        5. If the user provides OUTPUT from a command:
           - Analyze the output and summarize it in simple, human-readable English.
           - ignore technical jargon unless necessary.
           - Start with "Here is the summary/status:" or similar.
        """
        
        # Initial setup - use retry to avoid crashing start-up
        try:
            self._send_with_retry(self.system_instruction)
        except Exception as e:
            console.print(f"[red]Warning: Failed to initialize AI context ({e}). proceeding in basic mode.[/red]")

    def is_configured(self):
        return bool(self.api_key)

    def _send_with_retry(self, message: str):
        """
        Sends a message with exponential backoff for 429 errors.
        """
        max_retries = 3
        
        for attempt in range(max_retries):
            try:
                return self.chat.send_message(message)
            except Exception as e:
                error_str = str(e)
                # Check for 429 Quota Exceeded
                if "429" in error_str and attempt < max_retries - 1:
                    wait_time = (attempt + 1) * 5  # Wait 5s, 10s, 15s...
                    console.print(f"[yellow]Rate limit hit. Waiting {wait_time}s...[/yellow]")
                    time.sleep(wait_time)
                    continue
                elif attempt == max_retries - 1:
                    raise e
                else:
                    raise e

    def get_response(self, user_input: str) -> dict:
        """
        Returns a dict:
        {
           "type": "command" | "text",
           "content": str (command or text response),
           "explanation": str (optional)
        }
        """
        try:
            response = self._send_with_retry(user_input)
            text = response.text.strip()
            
            # Parse for COMMAND: format
            if "COMMAND:" in text:
                lines = text.split('\n')
                cmd = ""
                explanation = ""
                for line in lines:
                    if line.strip().startswith("COMMAND:"):
                        cmd = line.replace("COMMAND:", "").strip()
                    elif line.strip().startswith("EXPLANATION:"):
                        explanation = line.replace("EXPLANATION:", "").strip()
                
                return {
                    "type": "command",
                    "content": cmd,
                    "explanation": explanation
                }
            else:
                return {
                    "type": "text",
                    "content": text
                }
        except Exception as e:
            return {
                "type": "error",
                "content": f"AI Error: {str(e)}"
            }

    def summarize_output(self, original_request: str, command: str, output: str) -> str:
        """
        Sends the command output back to LLM for summarization.
        """
        prompt = f"""
        CONTEXT:
        User Request: "{original_request}"
        Executed Command: "{command}"
        
        COMMAND OUTPUT:
        {output}
        
        INSTRUCTION:
        Summarize the above output for the user in clear, non-technical English. 
        Highlight key details (like IDs, errors, or status).
        """
        try:
            response = self._send_with_retry(prompt)
            return response.text
        except Exception as e:
            return f"Error analyzing output: {e}"
