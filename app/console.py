# app/console.py

from rich.console import Console
from rich.panel import Panel
from rich.live import Live
from rich.spinner import Spinner
from rich.table import Table
from rich.align import Align
import time
import os

console = Console()

def clear():
    """Membersihkan layar terminal."""
    os.system('clear')

def print_cyber_panel(title: str, subtitle: str = ""):
    """Mencetak panel pembuka dengan gaya cyber."""
    panel = Panel(
        Align.center(f"[bold cyan]{title}[/bold cyan]\n[dim]{subtitle}[/dim]"),
        title="[bold green]◈ MY-TERMUX-TOOL ◈[/bold green]",
        border_style="bright_blue",
        padding=(1, 2),
    )
    console.print(panel)

def cyber_input(prompt: str) -> str:
    """Mendapatkan input dari user dengan gaya konsisten dan menghapus spasi."""
    return console.input(f"[bold pale_turquoise1]>> {prompt}[/bold pale_turquoise1]: ").strip()

def loading_animation(task_name: str, duration: int = 2):
    """Menampilkan animasi loading untuk sebuah tugas."""
    with Live(Spinner("dots12", text=f"[bold yellow]Processing {task_name}...[/bold yellow]"), refresh_per_second=10) as live:
        time.sleep(duration)
    console.print(f"[bold green]✓[/bold green] [bold white]{task_name} completed.[/bold white]")

def create_menu_table(title: str, options: list) -> Table:
    """Membuat Tabel Menu yang sudah di-style."""
    table = Table(show_header=True, header_style="bold bright_magenta", title=title, title_style="bold cyan", title_justify="center")
    table.add_column("No.", style="dim", width=4)
    table.add_column("Menu", style="bold white")
    
    for i, option in enumerate(options):
        table.add_row(str(i + 1), option)
    
    table.add_row("0", "[bold red]Back[/bold red]")
    return table