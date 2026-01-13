import psutil
from rich.table import Table
from rich.panel import Panel
from rich.console import Console
from rich import box
import os

console = Console()

def get_system_status() -> Panel:
    """
    Returns a Rich Panel containing system health statistics.
    """
    # CPU
    cpu_percent = psutil.cpu_percent(interval=1)
    cpu_count = psutil.cpu_count(logical=True)
    
    # Memory
    mem = psutil.virtual_memory()
    mem_total = mem.total / (1024 ** 3)
    mem_used = mem.used / (1024 ** 3)
    mem_percent = mem.percent

    # Disk
    disk = psutil.disk_usage('/')
    disk_total = disk.total / (1024 ** 3)
    disk_free = disk.free / (1024 ** 3)
    disk_percent = disk.percent
    
    # Create Table
    table = Table(box=box.SIMPLE)
    table.add_column("Metric", style="cyan", no_wrap=True)
    table.add_column("Value", style="magenta")
    table.add_column("Status", style="green")

    # CPU Row
    cpu_status = "[green]OK[/green]" if cpu_percent < 80 else "[red]HIGH LOAD[/red]"
    table.add_row("CPU Usage", f"{cpu_percent}% ({cpu_count} Cores)", cpu_status)

    # Memory Row
    mem_status = "[green]OK[/green]" if mem_percent < 85 else "[red]LOW MEMORY[/red]"
    table.add_row("Memory", f"{mem_used:.1f}GB / {mem_total:.1f}GB ({mem_percent}%)", mem_status)

    # Disk Row
    disk_status = "[green]OK[/green]" if disk_percent < 90 else "[red]LOW SPACE[/red]"
    table.add_row("Disk (Root)", f"{disk_free:.1f}GB Free / {disk_total:.1f}GB Total", disk_status)

    return Panel(table, title="[bold blue]System Status[/bold blue]", border_style="blue")
