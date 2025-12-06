# menu/downloader/main.py

from .functions.bilibili_downloader import bilibili_downloader
from .functions.youtube_mp3_downloader import youtube_mp3_downloader
from .functions.youtube_mp4_downloader import youtube_mp4_downloader
from .functions.spotify_downloader import spotify_downloader
from .functions.soundcloud_downloader import soundcloud_downloader
from .functions.facebook_downloader import facebook_downloader
from .functions.threads_downloader import threads_downloader
from .functions.instagram_downloader import instagram_downloader
from .functions.mega_downloader import mega_downloader
from .functions.tiktok_downloader import tiktok_downloader
from .functions.tiktok_downloader_v2 import tiktok_downloader_v2
from .functions.mediafire_downloader import mediafire_downloader
from .functions.krakenfiles_downloader import krakenfiles_downloader
from .functions.gdrive_downloader import gdrive_downloader
from .functions.twitter_downloader import twitter_downloader
from app.console import console, cyber_input, clear
from rich.table import Table
from rich.panel import Panel
from rich.box import SQUARE

def main():
    """Fungsi utama untuk menu Downloader. Ini yang dipanggil oleh main.py."""
    menu_actions = {
        '1': bilibili_downloader,
        '2': youtube_mp3_downloader,
        '3': youtube_mp4_downloader,
        '4': spotify_downloader,
        '5': soundcloud_downloader,
        '6': facebook_downloader,
        '7': threads_downloader,
        '8': instagram_downloader,
        '9': mega_downloader,
        '10': tiktok_downloader,
        '11': tiktok_downloader_v2,
        '12': mediafire_downloader,
        '13': krakenfiles_downloader,
        '14': gdrive_downloader,
        '15': twitter_downloader,
    }

    while True:
        clear()
        
        table = Table(
            show_header=True,
            header_style="bold #00F0FF",
            title="[bold magenta]📥 Downloader Tools 📥[/bold magenta]",
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
        downloader_options = [
            {"name": "Bilibili DL", "desc": "Unduh video dari Bilibili."},
            {"name": "YouTube MP3 DL", "desc": "Unduh audio dari YouTube."},
            {"name": "YouTube MP4 DL", "desc": "Unduh video dari YouTube."},
            {"name": "Spotify DL", "desc": "Unduh audio dari Spotify."},
            {"name": "SoundCloud DL", "desc": "Unduh audio dari SoundCloud."},
            {"name": "Facebook DL", "desc": "Unduh dari Facebook."},
            {"name": "Threads DL", "desc": "Unduh media (gambar/video) dari Threads."},
            {"name": "Instagram DL", "desc": "Unduh media (gambar/video) dari Instagram."},
            {"name": "Mega DL", "desc": "Unduh file/folder dari Mega.nz."},
            {"name": "Tiktok DL", "desc": "Unduh video/audio dari TikTok."},
            {"name": "Tiktok DL (v2)", "desc": "Unduh video/audio dari TikTok (API v2)."},
            {"name": "MediaFire DL", "desc": "Unduh file dari MediaFire."},
            {"name": "KrakenFiles DL", "desc": "Unduh file dari KrakenFiles."},
            {"name": "Google Drive DL", "desc": "Unduh file dari Google Drive."},
            {"name": "Twitter DL", "desc": "Unduh media (gambar/video) dari Twitter."},
        ]
        
        for i, item in enumerate(downloader_options):
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

        choice = cyber_input("Pilih alat Downloader")

        if choice in menu_actions:
            menu_actions[choice]()
        elif choice in ['0', 'b']:
            break
        else:
            console.print("[bold red]Pilihan tidak valid![/bold red]")
            cyber_input("Tekan Enter untuk melanjutkan...")