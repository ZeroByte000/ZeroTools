# main.py

import sys
import os

# Tambahkan root project ke Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.align import Align
from rich.text import Text

# Import fungsi gaya dan input dari app/console
from app.console import console, cyber_input, clear

# Import FUNGSI main dari setiap sub-menu
from menu.ai import main as ai_menu
# ... (import lainnya dikomentari untuk sementara)

# --- PERUBAHAN: Import fungsi load_config ---
from core.utils import load_config

# --- Konfigurasi Menu dan Tampilan ---

# ASCII Art untuk header
HEADER_ART = """
[bold cyan]
  [bold yellow]██╗    ██╗██╗  ██╗ █████╗ ████████╗[/bold yellow]
  [bold yellow]██║    ██║██║  ██║██╔══██╗╚══██╔══╝[/bold yellow]
  [bold yellow]██║ █╗ ██║███████║███████║   ██║[/bold yellow]
  [bold yellow]██║███╗██║██╔══██║██╔══██║   ██║[/bold yellow]
  [bold yellow]╚███╔███╔╝██║  ██║██║  ██║   ██║[/bold yellow]
  [bold yellow] ╚══╝╚══╝ ╚═╝  ╚═╝╚═╝  ╚═╝   ╚═╝[/bold yellow]
        [bold green]Termux Utility Tool[/bold green]
[/bold cyan]
"""

# Data menu dengan ikon dan deskripsi
MENU_DATA = [
    {"name": "AI", "icon": "🤖", "desc": "Kecerdasan buatan, Chat, Image Gen."},
#    {"name": "Tools", "icon": "🛠️", "desc": "Alat bantu umum (Hash, QR, dll.)."},
#    {"name": "Uploader", "icon": "📤", "desc": "Unggah file ke berbagai host."},
#    {"name": "Downloader", "icon": "📥", "desc": "Unduh media dari berbagai platform."},
#    {"name": "Search", "icon": "🔍", "desc": "Pencarian informasi dan media."},
#    {"name": "Stalk", "icon": "🕵️", "desc": "Dapatkan informasi pengguna (OSINT)."},
#    {"name": "Image", "icon": "🖼️", "desc": "Manipulasi dan pengolahan gambar."},
#    {"name": "Weebs", "icon": "🎌", "desc": "Aneka tools untuk para wibu."},
#    {"name": "Otakudesu", "icon": "🍜", "desc": "Unduh anime dari Otakudesu."},
#    {"name": "Misc", "icon": "🎲", "desc": "Aneka menu serbaguna lainnya."},
]

# Pemetaan input pengguna ke fungsi menu
MENU_ACTIONS = {
    '1': ai_menu,
#    '2': tools_menu,
#    ... (lainnya dikomentari)
}

# --- Fungsi Pembuat Komponen Tampilan ---

def create_header() -> Panel:
    """Membuat panel header dengan ASCII art."""
    header_text = Text.from_markup(HEADER_ART, justify="center")
    return Panel(header_text, border_style="bright_blue", padding=(1, 2))

def create_menu_table() -> Table:
    """Membuat tabel menu utama yang diperkaya."""
    table = Table(
        show_header=True,
        header_style="bold magenta",
        title="[bold green]◈ Main Menu ◈[/bold green]",
        title_style="bold green",
        show_lines=True,
        expand=True,
        box=None
    )
    table.add_column("No.", style="bold cyan", width=4, justify="center")
    table.add_column("Menu", style="bold white", min_width=15)
    table.add_column("Deskripsi", style="dim", min_width=35)

    for i, item in enumerate(MENU_DATA):
        table.add_row(
            str(i + 1),
            f"{item['icon']} {item['name']}",
            item['desc']
        )
    
    table.add_row("0", "[bold red]🚪 Keluar[/bold red]", "[dim red]Menutup aplikasi.[/dim red]")
    return table

# --- PERUBAHAN: Ganti fungsi footer untuk menampilkan kredit ---
def create_credits_footer(author: str, github_url: str) -> Panel:
    """Membuat footer dengan informasi author dan GitHub."""
    credits_text = f"[bold cyan]Author:[/bold cyan] [bold white]{author}[/bold white] | [bold cyan]GitHub:[/bold cyan] [link={github_url}]{github_url}[/link]"
    return Panel(credits_text, border_style="dim", padding=(0, 1))

# --- Fungsi Utama Aplikasi ---

def main():
    """Fungsi utama untuk menjalankan aplikasi."""
    # --- PERUBAHAN: Muat konfigurasi di awal fungsi ---
    config = load_config()

    while True:
        clear()
        console.print(create_header())
        console.print(create_menu_table())
        
        # --- PERUBAHAN: Tampilkan footer kredit jika konfigurasi ada ---
        if config and config.get("author") and config.get("github"):
            console.print(create_credits_footer(config["author"], config["github"]))
        else:
            # Tampilkan pesan default jika konfigurasi tidak ditemukan
            console.print(Panel("[dim]Author information not found.[/dim]", border_style="dim", padding=(0, 1)))
        
        choice = cyber_input("Pilih menu")

        if choice in MENU_ACTIONS:
            # Jalankan fungsi yang sesuai dengan pilihan
            MENU_ACTIONS[choice]()
        elif choice in ['0', 'q', 'exit']:
            # Tampilkan pesan keluar yang menarik
            console.print("\n[bold red]Terima kasih telah menggunakan tools ini![/bold red]")
            console.print("[bold cyan]Sampai jumpa lagi! 👋[/bold cyan]\n")
            sys.exit()
        else:
            console.print("\n[bold yellow]Pilihan tidak valid. Silakan coba lagi.[/bold yellow]")
            cyber_input("Tekan Enter untuk melanjutkan...")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        # Tangkap sinyal Ctrl+C dan tampilkan pesan keluar yang rapi
        console.print("\n[yellow]Program dihentikan oleh pengguna.[/yellow]")
        console.print("[cyan]Sampai jumpa lagi! 👋[/cyan]\n")
        sys.exit()