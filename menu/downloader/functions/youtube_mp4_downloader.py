# menu/downloader/functions/youtube_mp4_downloader.py

import os
import requests
import json
from urllib.parse import quote
from datetime import datetime
from core.utils import load_config, get_output_path
from app.console import console, print_cyber_panel, cyber_input, clear
from rich.table import Table
from rich.panel import Panel
from rich.box import SQUARE
from rich.text import Text
from rich.console import Group

def display_youtube_info(data):
    info_items = []
    
    title = data.get("title", "Unknown Title")
    author = data.get("author", "Unknown Author")
    author_url = data.get("authorUrl", "")
    length_seconds = data.get("lengthSeconds", 0)
    views = data.get("views", 0)
    upload_date = data.get("uploadDate", "Unknown")
    thumbnail = data.get("thumbnail", "")
    video_quality = data.get("quality", "Unknown")
    
    info_items.append(Text.assemble(("Judul: ", "bold cyan"), (title, "white")))
    info_items.append(Text.assemble(("Author: ", "bold cyan"), (author, "white")))
    if author_url:
        info_items.append(Text.assemble(("Author URL: ", "bold cyan"), (author_url, "white")))
    info_items.append(Text.assemble(("Durasi: ", "bold cyan"), (f"{length_seconds} detik", "white")))
    info_items.append(Text.assemble(("Ditonton: ", "bold cyan"), (f"{views} kali", "white")))
    info_items.append(Text.assemble(("Diunggah: ", "bold cyan"), (upload_date, "white")))
    info_items.append(Text.assemble(("Kualitas: ", "bold cyan"), (video_quality, "white")))
    
    if thumbnail:
        info_items.append(Text.assemble(("Thumbnail: ", "bold cyan"), (thumbnail, "white")))
    
    info_group = Group(*info_items)
    
    panel = Panel(
        info_group,
        title="[bold magenta]🎬 Informasi Video 🎬[/bold magenta]",
        border_style="medium_purple",
        padding=(1, 2)
    )
    console.print(panel)

def get_video_quality() -> str:

    quality_options = [
        {"name": "360p", "value": "360"},
        {"name": "480p", "value": "480"},
        {"name": "720p (HD)", "value": "720"},
        {"name": "1080p (Full HD)", "value": "1080"},
    ]

    while True:

        
        table = Table(
            show_header=True,
            header_style="bold cyan",
            title="[bold magenta]🎬 Pilih Kualitas Video 🎬[/bold magenta]",
            title_style="bold magenta",
            title_justify="center",
            box=SQUARE,
            show_lines=True,
            expand=True,
            padding=(0, 1)
        )
        table.add_column("No.", style="bold cyan", width=4, justify="center")
        table.add_column("Kualitas", style="bold cyan", min_width=25)
        
        for i, option in enumerate(quality_options):
            table.add_row(str(i + 1), option['name'])
        
        table.add_row("0", "[bold yellow]← Kembali[/bold yellow]")
        
        panel = Panel(
            table,
            border_style="medium_purple",
            padding=(1, 1)
        )
        console.print(panel)
        
        console.print("[dim]Pilih kualitas video yang ingin diunduh.[/dim]")
        console.print("[dim]Gunakan '0' atau 'b' untuk kembali.[/dim]")

        choice = cyber_input("Masukkan nomor pilihan")
        
        if choice in ['0', 'b']:
            return None # Kembali
        
        if choice.isdigit() and 1 <= int(choice) <= len(quality_options):
            return quality_options[int(choice) - 1]['value']
        
        console.print("[bold red]Pilihan tidak valid![/bold red]")
        cyber_input("Tekan Enter untuk mencoba lagi...")

def youtube_mp4_downloader():

    clear()
    print_cyber_panel("YouTube MP4 Downloader", "Unduh video dari YouTube dengan pilihan kualitas")
    
    url_input = cyber_input("URL YouTube (contoh: https://youtu.be/QXEcKthUIwI) atau ketik '00' untuk kembali")
    
    if url_input == '00':
        return

    quality = get_video_quality()
    if quality is None:
        return 

    try:
        with console.status("[bold green]Mengambil informasi video...[/bold green]", spinner="dots"):
            config = load_config()
            if not config or not config.get("base_url"):
                console.print("[bold red]Error: Konfigurasi atau base_url tidak ditemukan.[/bold red]")
                cyber_input("Tekan Enter untuk kembali...")
                return

            base_url = config.get("base_url")
            api_endpoint = f"{base_url}/api/downloader/ytmp4"

            encoded_url = quote(url_input)
            
            response = requests.get(f"{api_endpoint}?url={encoded_url}&quality={quality}")
            response.raise_for_status()
            result = response.json()

        if result.get("title"):

            display_youtube_info(result)
            
            download_url = result.get("url", "")
            video_quality = result.get("quality", "Unknown")
            
            if not download_url:
                console.print("[bold red]URL unduhan tidak tersedia untuk kualitas ini.[/bold red]")
                cyber_input("Tekan Enter untuk kembali...")
                return

            safe_title = "".join(c for c in result.get('title', 'video') if c.isalnum() or c in (' ', '-', '_')).rstrip()
            filename = f"{safe_title}_{video_quality}.mp4"

            output_path = get_output_path("downloads", filename)

            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
            }

            with console.status("[bold green]Mengunduh video...[/bold green]", spinner="dots"):
                video_response = requests.get(download_url, stream=True, headers=headers)
                video_response.raise_for_status()
                
                with open(output_path, 'wb') as f:
                    for chunk in video_response.iter_content(chunk_size=8192):
                        f.write(chunk)
            
            console.print(f"\n[bold green]✓ Video berhasil diunduh![/bold green]")
            console.print(f"[bold cyan]Lokasi:[/bold cyan] {output_path}")

            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            log_filename = f"youtube_mp4_download_log_{timestamp}.json"
            log_path = get_output_path("output", log_filename, no_prompt=True)
            
            with open(log_path, 'w') as f:
                json.dump(result, f, indent=4)
            
            console.print(f"[dim]Log respons disimpan di: {log_path}[/dim]")
        else:
            console.print(f"[bold red]Gagal mengambil informasi video.[/bold red]")
            console.print(f"Detail dari server: {result}")

    except requests.exceptions.RequestException as e:
        console.print(f"\n[bold red]Error saat menghubungi API:[/bold red] {e}")
    except Exception as e:
        console.print(f"\n[bold red]Terjadi kesalahan tak terduga:[/bold red] {e}")
        
    cyber_input("\nTekan Enter untuk kembali ke menu...")