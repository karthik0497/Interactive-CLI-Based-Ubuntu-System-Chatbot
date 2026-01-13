import typer
import os
from rich.console import Console
from rich.panel import Panel
from rich.prompt import Prompt
from modules.system_checker import get_system_status
from modules.executor import execute_command
from modules.ai_engine import AIEngine
from dotenv import load_dotenv

# Load env variables
load_dotenv()

app = typer.Typer()
console = Console()

def setup_api_key():
    """
    Check for API key, if missing ask user.
    """
    if not os.getenv("GEMINI_API_KEY"):
        console.print(Panel("To make this chatbot intelligent, you need a Google Gemini API Key.\nGet it for free at: [link=https://aistudio.google.com/app/apikey]https://aistudio.google.com/app/apikey[/link]", title="API Key Required", border_style="red"))
        key = Prompt.ask("Enter your GEMINI_API_KEY", password=True)
        if key:
            # Set for current session
            os.environ["GEMINI_API_KEY"] = key
            # Save to .env for future
            with open(".env", "a") as f:
                f.write(f"\nGEMINI_API_KEY={key}\n")
            console.print("[green]API Key saved![/green]")
        else:
            console.print("[yellow]No API Key provided. Falling back to dumb mode.[/yellow]")

@app.command()
def start():
    """
    Starts the Intelligent Ubuntu System Chatbot.
    """
    console.clear()
    console.print(Panel("[bold green]Welcome to the Intelligent Ubuntu System Chatbot[/bold green]\nType [bold red]'exit'[/bold red] to quit.", title="Antigravity Assistant"))
    
    setup_api_key()
    
    # Initialize AI
    try:
        ai = AIEngine()
        has_ai = ai.is_configured()
    except Exception as e:
        console.print(f"[red]Failed to initialize AI: {e}[/red]")
        has_ai = False

    while True:
        try:
            user_input = console.input("[bold cyan]You > [/bold cyan]")
            
            if user_input.lower() in ["exit", "quit"]:
                console.print("[yellow]Goodbye![/yellow]")
                break
            
            if user_input.lower() in ["status", "check system", "health"]:
                console.print(get_system_status())
                continue
            
            if user_input.lower() == "enable autostart":
                from modules.startup_manager import enable_autostart
                enable_autostart()
                continue
                
            if user_input.lower() == "disable autostart":
                from modules.startup_manager import disable_autostart
                disable_autostart()
                continue

            if has_ai:
                with console.status("[bold green]Thinking...[/bold green]", spinner="dots"):
                    response = ai.get_response(user_input)

                if response["type"] == "text":
                    console.print(f"[bold magenta]AI:[/bold magenta] {response['content']}")
                
                elif response["type"] == "command":
                    cmd = response["content"]
                    expl = response.get("explanation", "")
                    
                    if expl:
                        console.print(f"[dim]Reasoning: {expl}[/dim]")
                    
                    # Execute
                    success, output = execute_command(cmd)
                    
                    if output.strip():
                        with console.status("[bold green]Analyzing Output...[/bold green]", spinner="dots"):
                            summary = ai.summarize_output(user_input, cmd, output)
                        
                        title = "AI Summary" if success else "AI Error Analysis & Fix"
                        style = "magenta" if success else "red"
                        console.print(Panel(summary, title=title, border_style=style))
                
                elif response["type"] == "error":
                     console.print(f"[red]AI Error: {response['content']}[/red]")

            else:
                 # Fallback for no API Key
                 console.print("[dim]AI is not configured. I can only run 'status'. Set GEMINI_API_KEY to enable smart features.[/dim]")

        except KeyboardInterrupt:
            console.print("\n[yellow]Goodbye![/yellow]")
            break

if __name__ == "__main__":
    app()
