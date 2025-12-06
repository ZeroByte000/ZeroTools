# menu/downloader/functions/youtube_mp3_downloader.py

import os
import requests
import json
from urllib.parse import quote
from datetime import datetime
from core.utils import load_config, get_output_path
from app.console import console, print_cyber_panel, cyber_input, clear
from rich.panel import Panel
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
    description = data.get("description", "No Description")
    quality = data.get("quality", "Unknown")
    
    info_items.append(Text.assemble(("Judul: ", "bold cyan"), (title, "white")))
    info_items.append(Text.assemble(("Author: ", "bold cyan"), (author, "white")))
    if author_url:
        info_items.append(Text.assemble(("Author URL: ", "bold cyan"), (author_url, "white")))
    info_items.append(Text.assemble(("Durasi: ", "bold cyan"), (f"{length_seconds} detik", "white")))
    info_items.append(Text.assemble(("Ditonton: ", "bold cyan"), (f"{views} kali", "white")))
    info_items.append(Text.assemble(("Diunggah: ", "bold cyan"), (upload_date, "white")))
    info_items.append(Text.assemble(("Kualitas: ", "bold cyan"), (quality, "white")))
    
    if thumbnail:
        info_items.append(Text.assemble(("Thumbnail: ", "bold cyan"), (thumbnail, "white")))
    
    info_group = Group(*info_items)
    
    panel = Panel(
        info_group,
        title="[bold magenta]🎵 Informasi Video 🎵[/bold magenta]",
        border_style="medium_purple",
        padding=(1, 2)
    )
    console.print(panel)

def youtube_mp3_downloader():

    clear()
    print_cyber_panel("YouTube MP3 Downloader", "Unduh audio dari YouTube dalam format MP3")
    
    url_input = cyber_input("URL YouTube (contoh: https://youtu.be/QXEcKthUIwI) atau ketik '00' untuk kembali")
    
    if url_input == '00':
        return

    try:
        with console.status("[bold green]Mengambil informasi video...[/bold green]", spinner="dots"):
            config = load_config()
            if not config or not config.get("base_url"):
                console.print("[bold red]Error: Konfigurasi atau base_url tidak ditemukan.[/bold red]")
                cyber_input("Tekan Enter untuk kembali...")
                return

            base_url = config.get("base_url")
            api_endpoint = f"{base_url}/api/downloader/ytmp3"
            
            encoded_url = quote(url_input)
            
            response = requests.get(f"{api_endpoint}?url={encoded_url}")
            response.raise_for_status()
            result = response.json()

        if result.get("title"):

            display_youtube_info(result)
            
            download_url = result.get("url", "")
            
            if not download_url:
                console.print("[bold red]URL unduhan tidak tersedia.[/bold red]")
                cyber_input("Tekan Enter untuk kembali...")
                return
            
            safe_title = "".join(c for c in result.get('title', 'youtube_audio') if c.isalnum() or c in (' ', '-', '_')).rstrip()
            filename = f"{safe_title}.mp3"
            
            output_path = get_output_path("downloads", filename)
            
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
            }

            with console.status("[bold green]Mengunduh audio...[/bold green]", spinner="dots"):
                audio_response = requests.get(download_url, stream=True, headers=headers)
                audio_response.raise_for_status()
                
                with open(output_path, 'wb') as f:
                    for chunk in audio_response.iter_content(chunk_size=8192):
                        f.write(chunk)
            
            console.print(f"\n[bold green]✓ Audio berhasil diunduh![/bold green]")
            console.print(f"[bold cyan]Lokasi:[/bold cyan] {output_path}")

            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            log_filename = f"youtube_mp3_download_log_{timestamp}.json"
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