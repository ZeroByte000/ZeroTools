# main.py

import sys
import os

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.align import Align
from rich.text import Text
from pyfiglet import figlet_format
from app.console import console, cyber_input, clear
from menu.ai import main as ai_menu
from menu.uploader import main as uploader_menu
from menu.downloader import main as downloader_menu
from core.utils import load_config

HEADER_ART_TEMPLATE = """
[bold #00F0FF]{author_ascii_art}[/bold #00F0FF]
"""

MENU_DATA = [
    {"name": "AI", "icon": "🤖", "desc": "Kecerdasan buatan, Chat, Image Gen."},
    {"name": "Uploader", "icon": "📤", "desc": "Unggah file ke berbagai host."},
    {"name": "Downloader", "icon": "📥", "desc": "Unduh video dari berbagai platform."},
]


MENU_ACTIONS = {
    '1': ai_menu,
    '2': uploader_menu,
    '3': downloader_menu,
}


def create_header(author_name: str) -> Panel:
    display_name = author_name if author_name else "ZeroTools"
    
    try:
        author_ascii_art = figlet_format(display_name, font='slant')
    except Exception:
        author_ascii_art = display_name

    header_art = HEADER_ART_TEMPLATE.format(author_ascii_art=author_ascii_art)
    header_text = Text.from_markup(header_art, justify="center")
    return Panel(Align.center(header_text), border_style="#00F0FF", padding=(1, 2))

def create_menu_table() -> Table:
    table = Table(
        show_header=False,
        show_lines=True,
        expand=True,
        box=None
    )

    table.add_column("No.", style="bold white", width=4, justify="center")
    table.add_column("Menu", style="bold white", min_width=15)
    table.add_column("Deskripsi", style="white", min_width=35)

    for i, item in enumerate(MENU_DATA):
        table.add_row(
            str(i + 1),
            f"{item['icon']} {item['name']}",
            item['desc']
        )
    
    table.add_row("0", "[bold red]🚪 Keluar[/bold red]", "[red]Menutup aplikasi.[/red]")
    return table

def create_credits_footer(author: str, github_url: str) -> Panel:

    credits_text = f"[bold #00F0FF]Author:[/bold #00F0FF] [bold white]{author}[/bold white] | [bold #00F0FF]GitHub:[/bold #00F0FF] [link={github_url}]{github_url}[/link]"

    return Panel(Align.center(credits_text), border_style="#00F0FF", padding=(0, 1))

def main():

    config = load_config()
    
    author_name = config.get("author", "ZeroTools") if config else "ZeroTools"

    while True:
        clear()

        console.print(create_header(author_name))

        menu_table = create_menu_table()
        menu_panel = Panel(
            Align.center(menu_table),
            title="[bold #00F0FF]◈ Main Menu ◈[/bold #00F0FF]",
            title_align="center",
            border_style="#00F0FF",
            padding=(1, 2)
        )
        
        console.print(menu_panel)
        
        if config and config.get("author") and config.get("github"):
            console.print(create_credits_footer(config["author"], config["github"]))
        else:
            console.print(Panel(Align.center("[dim]Author information not found.[/dim]"), border_style="#00F0FF", padding=(0, 1)))
        
        choice = cyber_input("Pilih menu")

        if choice in MENU_ACTIONS:
            MENU_ACTIONS[choice]()
        elif choice in ['0', 'q', 'exit']:
            console.print("\n[bold red]Terima kasih telah menggunakan tools ini![/bold red]")
            console.print("[bold #00F0FF]Sampai jumpa lagi! 👋[/bold #00F0FF]\n")
            sys.exit()
        else:
            console.print("\n[bold yellow]Pilihan tidak valid. Silakan coba lagi.[/bold yellow]")
            cyber_input("Tekan Enter untuk melanjutkan...")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        console.print("\n[yellow]Program dihentikan oleh pengguna.[/yellow]")
        console.print("[#00F0FF]Sampai jumpa lagi! 👋[/#00F0FF]\n")
        sys.exit()