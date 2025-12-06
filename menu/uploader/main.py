# menu/uploader/main.py

from .functions.image_db_uploader import image_db_uploader
from app.console import console, cyber_input, clear
from rich.table import Table
from rich.panel import Panel
from rich.box import SQUARE

def main():

    menu_actions = {
        '1': image_db_uploader,
    }

    while True:
        clear()
        
        table = Table(
            show_header=True,
            header_style="bold #00F0FF",
            title="[bold magenta]📤 Uploader Tools 📤[/bold magenta]",
            title_style="bold magenta",
            title_justify="center",
            box=SQUARE,
            border_style="#00F0FF",
            show_lines=True,
            expand=True,
            padding=(0, 1)
        )
        table.add_column("No.", style="bold white", width=4, justify="center")
        table.add_column("Menu", style="bold white", overflow=None)
        table.add_column("Deskripsi", style="bold white", overflow=None)
        uploader_options = [
            {"name": "Image DB Uploader", "desc": "Unggah gambar ke ImgBB dengan opsi kedaluwarsa."},
        ]
        
        for i, item in enumerate(uploader_options):
            table.add_row(
                str(i + 1),
                item['name'],
                item['desc']
            )

        table.add_row("0", "[bold yellow]← Kembali[/bold yellow]", "[bold white]Kembali ke menu utama.[/bold white]")
        panel = Panel(
            table,
            border_style="#00F0FF",
            padding=(1, 1)
        )
        console.print(panel)
        
        console.print("[dim]Gunakan '0' atau 'b' untuk kembali.[/dim]")

        choice = cyber_input("Pilih alat Uploader")

        if choice in menu_actions:
            menu_actions[choice]()
        elif choice in ['0', 'b']:
            break 
        else:
            console.print("[bold red]Pilihan tidak valid![/bold red]")
            cyber_input("Tekan Enter untuk melanjutkan...")