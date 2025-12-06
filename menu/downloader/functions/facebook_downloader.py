# menu/downloader/functions/facebook_downloader.py

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

def get_video_quality(video_data):

    while True:
        clear()

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
        table.add_column("Kualitas", style="bold cyan", min_width=20)
        table.add_column("Tipe", style="bold cyan", min_width=10)
        
        for i, video in enumerate(video_data):
            table.add_row(str(i + 1), video['resolution'], video['type'])
        
        table.add_row("0", "[bold yellow]← Kembali[/bold yellow]", "")
        
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
            return None
        
        if choice.isdigit() and 1 <= int(choice) <= len(video_data):
            return video_data[int(choice) - 1]
        
        console.print("[bold red]Pilihan tidak valid![/bold red]")
        cyber_input("Tekan Enter untuk mencoba lagi...")

def facebook_downloader():

    clear()
    print_cyber_panel("Facebook Downloader", "Unduh video dari Facebook")

    url_input = cyber_input("URL Facebook (contoh: https://www.facebook.com/share/...) atau ketik '00' untuk kembali")
    
    if url_input == '00':
        return

    try:
        with console.status("[bold green]Mengambil informasi video...[/bold green]", spinner="dots"):
            config = load_config()
            if not config:
                console.print("[bold red]Error: Gagal memuat konfigurasi. Pastikan file 'core/config.json' ada dan valid.[/bold red]")
                cyber_input("Tekan Enter untuk kembali...")
                return

            base_url = config.get("base_url")
            if not base_url:
                console.print("[bold red]Error: 'base_url' tidak ditemukan di 'core/config.json'.[/bold red]")
                cyber_input("Tekan Enter untuk kembali...")
                return

            api_endpoint = f"{base_url}/api/downloader/fbdl"
            
            encoded_url = quote(url_input)
            
            response = requests.get(f"{api_endpoint}?url={encoded_url}")
            response.raise_for_status()
            result = response.json()

        if result.get("status"):
            video_data = result.get("data", [])
            
            if not video_data:
                console.print("[bold red]Tidak ada video yang tersedia untuk diunduh.[/bold red]")
                cyber_input("Tekan Enter untuk kembali...")
                return
            
            selected_video = get_video_quality(video_data)
            if selected_video is None:
                return 
            
            resolution = selected_video.get("resolution", "Unknown")
            video_url = selected_video.get("url", "")
            video_type = selected_video.get("type", "video")
            
            if not video_url:
                console.print("[bold red]URL unduhan tidak tersedia untuk kualitas ini.[/bold red]")
                cyber_input("Tekan Enter untuk kembali...")
                return
            
            console.print(f"\n[bold green]✓ Informasi video berhasil diambil![/bold green]")
            console.print(f"[bold cyan]Kualitas:[/bold cyan] {resolution}")
            console.print(f"[bold cyan]Tipe:[/bold cyan] {video_type}")
            
            safe_title = f"facebook_video_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
            if video_type == "video":
                filename = f"{safe_title}.mp4"
            else:
                filename = f"{safe_title}.jpg"
            
            output_path = get_output_path("downloads", filename)
            
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
            }

            with console.status("[bold green]Mengunduh video...[/bold green]", spinner="dots"):
                video_response = requests.get(video_url, stream=True, headers=headers)
                video_response.raise_for_status()
                
                with open(output_path, 'wb') as f:
                    for chunk in video_response.iter_content(chunk_size=8192):
                        f.write(chunk)
            
            console.print(f"\n[bold green]✓ Video berhasil diunduh![/bold green]")
            console.print(f"[bold cyan]Lokasi:[/bold cyan] {output_path}")

            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            log_filename = f"facebook_download_log_{timestamp}.json"
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