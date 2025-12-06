# menu/downloader/functions/bilibili_downloader.py

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

def display_video_info(data):
    info_items = []
    
    title = data.get("title", "Unknown Title")
    description = data.get("description", "No Description")
    locate = data.get("locate", "N/A")
    type_info = data.get("type", "N/A")
    views = data.get("views", "0")
    like = data.get("like", "0")
    cover = data.get("cover", "")

    media_list = data.get("mediaList", {})
    video_list = media_list.get("videoList", [])
    
    info_items.append(Text.assemble(("Judul: ", "bold cyan"), (title, "white")))
    info_items.append(Text.assemble(("Deskripsi: ", "bold cyan"), (description, "white")))
    info_items.append(Text.assemble(("Lokasi: ", "bold cyan"), (locate, "white")))
    info_items.append(Text.assemble(("Tipe: ", "bold cyan"), (type_info, "white")))
    info_items.append(Text.assemble(("Ditonton: ", "bold cyan"), (views, "white")))
    info_items.append(Text.assemble(("Suka: ", "bold cyan"), (like, "white")))
    
    if cover:
        info_items.append(Text.assemble(("Cover: ", "bold cyan"), (cover, "white")))
    
    if video_list:
        video_info = video_list[0]
        status = video_info.get("status", "N/A")
        filename = video_info.get("filename", "N/A")
        info_items.append(Text.assemble(("Status Unduhan: ", "bold cyan"), (status, "white")))
        info_items.append(Text.assemble(("Nama File: ", "bold cyan"), (filename, "white")))
    
    info_group = Group(*info_items)

    panel = Panel(
        info_group,
        title="[bold magenta]📹 Informasi Video 📹[/bold magenta]",
        border_style="medium_purple",
        padding=(1, 2)
    )
    console.print(panel)


def get_quality_choice(video_list):
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
        table.add_column("Kualitas", style="bold cyan", min_width=30)
        
        for i, video in enumerate(video_list):
            table.add_row(str(i + 1), video.get('filename', 'Unknown'))
        
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
            return None 
        
        if choice.isdigit() and 1 <= int(choice) <= len(video_list):
            return video_list[int(choice) - 1]
        
        console.print("[bold red]Pilihan tidak valid![/bold red]")
        cyber_input("Tekan Enter untuk mencoba lagi...")

def bilibili_downloader():

    clear()
    print_cyber_panel("Bilibili Downloader", "Unduh video dari Bilibili")
    
    url_input = cyber_input("URL Bilibili (contoh: https://www.bilibili.tv/id/video/4797649274017792) atau ketik '00' untuk kembali")
    
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
            api_endpoint = f"{base_url}/api/downloader/bilibili"
            
            encoded_url = quote(url_input)
            
            response = requests.get(f"{api_endpoint}?url={encoded_url}")
            response.raise_for_status()
            result = response.json()

        if result.get("status"):
            data = result.get("data", {})
            
            display_video_info(data)

            media_list = data.get("mediaList", {})
            video_list = media_list.get("videoList", [])
            
            if not video_list:
                console.print("[bold red]Tidak ada video yang tersedia untuk diunduh.[/bold red]")
                cyber_input("Tekan Enter untuk kembali...")
                return
            
            selected_video = get_quality_choice(video_list)
            if selected_video is None:
                return 
            
            video_url = selected_video.get("url")
            filename = selected_video.get("filename", f"bilibili_video_{datetime.now().strftime('%Y%m%d_%H%M%S')}.mp4")
            
            if not video_url:
                console.print("[bold red]URL video tidak tersedia.[/bold red]")
                cyber_input("Tekan Enter untuk kembali...")
                return
            
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
            log_filename = f"bilibili_download_log_{timestamp}.json"
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