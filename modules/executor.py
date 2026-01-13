import subprocess
from rich.console import Console
from rich.prompt import Confirm
from rich.panel import Panel

console = Console()

def execute_command(command: str) -> tuple[bool, str]:
    """
    Asks for user confirmation and then executes a shell command.
    Returns (success: bool, output: str)
    """
    console.print(Panel(f"[bold yellow]{command}[/bold yellow]", title="Proposed Command", border_style="yellow"))
    
    should_run = Confirm.ask("Do you want to execute this command?")
    
    if should_run:
        try:
            console.print(f"[dim]Executing: {command}[/dim]")
            # Using subprocess to run the command
            result = subprocess.run(
                command, 
                shell=True, 
                check=False, 
                text=True, 
                capture_output=True
            )
            
            output_str = ""
            if result.stdout:
                output_str += result.stdout + "\n"
                console.print(Panel(result.stdout, title="[green]Raw Output[/green]", border_style="green"))
            
            if result.stderr:
                output_str += "STDERR:\n" + result.stderr
                console.print(Panel(result.stderr, title="[red]Error Output[/red]", border_style="red"))
                
            if result.returncode == 0:
                 console.print("[bold green]Success![/bold green]")
                 return True, output_str
            else:
                 console.print(f"[bold red]Command failed with exit code {result.returncode}[/bold red]")
                 return False, output_str

        except Exception as e:
            console.print(f"[bold red]An error occurred during execution: {e}[/bold red]")
            return False, str(e)
    else:
        console.print("[bold red]Execution cancelled by user.[/bold red]")
        return False, "Cancelled by user"
