# menu/search/main.py

from .functions.bilibili_search import bilibili_search
from .functions.pinterest_search import pinterest_search
from .functions.wallpaper_search import wallpaper_search
from .functions.spotify_search import spotify_search
from .functions.youtube_search import youtube_search
from .functions.google_image_search import google_image_search
from .functions.bmkg_search import bmkg_search
from .functions.music_lyrics_search import music_lyrics_search
from .functions.mahasiswa_search import mahasiswa_search
from app.console import console, cyber_input, clear
from rich.table import Table
from rich.panel import Panel
from rich.box import SQUARE


def main():
    """Fungsi utama untuk menu Search."""
    menu_actions = {
        '1': bilibili_search,
        '2': pinterest_search,
        '3': wallpaper_search,
        '4': spotify_search,
        '5': youtube_search,
        '6': google_image_search,
        '7': bmkg_search,
        '8': music_lyrics_search,
        '9': mahasiswa_search,
    }

    while True:
        clear()
        
        table = Table(
            show_header=True,
            header_style="bold #00F0FF",
            title="[bold magenta]🔍 Search 🔍[/bold magenta]",
            title_style="bold magenta",
            title_justify="center",
            box=SQUARE,
            border_style="#00F0FF",
            show_lines=True,
            padding=(0, 1)
        )
        table.add_column("No.", style="bold white", width=4, justify="center")
        table.add_column("Menu", style="bold white", overflow=None)
        table.add_column("Deskripsi", style="bold white", overflow=None)

        search_options = [
            {"name": "Bilibili Search", "desc": "Cari video di platform Bilibili."},
            {"name": "Pinterest Search", "desc": "Cari gambar di platform Pinterest."},
            {"name": "Wallpaper Search", "desc": "Cari dan unduh wallpaper."},
            {"name": "Spotify Search", "desc": "Cari lagu di platform Spotify."},
            {"name": "YouTube Search", "desc": "Cari video di platform YouTube."},
            {"name": "Google Image Search", "desc": "Cari gambar di Google."},
            {"name": "BMKG", "desc": "Informasi dari BMKG."},
            {"name": "Music Lyrics", "desc": "Cari lirik lagu dari berbagai artis."},
            {"name": "Search Mahasiswa", "desc": "Cari data mahasiswa berdasarkan NIM atau nama."},
        ]
        
        for i, item in enumerate(search_options):
            table.add_row(
                str(i + 1),
                item['name'],
                item['desc']
            )
        
        table.add_row("0", "[bold yellow]← Kembali[/bold yellow]", "[bold #00F0FF]Kembali ke menu utama.[/bold #00F0FF]")

        panel = Panel(
            table,
            border_style="#00F0FF",  
            padding=(1, 1)
        )
        console.print(panel)

        console.print("[dim]Gunakan '0' atau 'b' untuk kembali.[/dim]")

        choice = cyber_input("Pilih layanan Pencarian")

        if choice in menu_actions:
            menu_actions[choice]()
        elif choice in ['0', 'b']:
            break  # Kembali ke menu utama
        else:
            console.print("[bold red]Pilihan tidak valid![/bold red]")
            cyber_input("Tekan Enter untuk melanjutkan...")