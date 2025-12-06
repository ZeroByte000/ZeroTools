# menu/downloader/functions/tiktok_downloader_v2.py

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

def format_duration(seconds):

    if seconds < 60:
        return f"00:{seconds:02d}"
    else:
        minutes = seconds // 60
        secs = seconds % 60
        return f"{minutes:02d}:{secs:02d}"

def display_video_info_v2(data):

    info_items = []
    
    title = data.get('desc', 'N/A')
    author_data = data.get("author", {})
    music_data = data.get("music", {})
    stats_data = data.get("stats", {}) 

    info_items.append(Text.assemble(("Judul: ", "bold cyan"), (title, "white")))
    
    author_name = author_data.get('nickname', 'N/A')
    author_id = author_data.get('unique_id', 'N/A')
    info_items.append(Text.assemble(("Author: ", "bold cyan"), (f"{author_name} (@{author_id})", "white")))
    info_items.append(Text.assemble(("Author ID: ", "bold cyan"), (author_data.get('uid', 'N/A'), "white")))

    info_items.append(Text.assemble(("Region: ", "bold cyan"), (author_data.get('region', 'N/A'), "white")))
    info_items.append(Text.assemble(("Durasi: ", "bold cyan"), (format_duration(music_data.get('duration', 0)), "white")))

    if music_data:
        music_title = music_data.get("title", "N/A")
        music_author = music_data.get("author", "N/A")
        info_items.append(Text.assemble(("Musik: ", "bold cyan"), (f"{music_title} oleh {music_author}", "white")))
    else:
        info_items.append(Text.assemble(("Musik: ", "bold cyan"), ("N/A", "white")))

    if stats_data:
        play_count = stats_data.get('play_count', 0)
        digg_count = stats_data.get('digg_count', 0)
        comment_count = stats_data.get('comment_count', 0)
        info_items.append(Text.assemble(("Dilihat: ", "bold cyan"), (f"{play_count:,} kali", "white")))
        info_items.append(Text.assemble(("Suka: ", "bold cyan"), (f"{digg_count:,}", "white")))
        info_items.append(Text.assemble(("Komentar: ", "bold cyan"), (f"{comment_count:,}", "white")))
    else:
        info_items.append(Text.assemble(("Statistik: ", "bold cyan"), ("N/A", "white")))

    info_group = Group(*info_items)

    panel = Panel(
        info_group,
        title="[bold magenta]📱 Informasi Video TikTok (v2) 📱[/bold magenta]",
        border_style="medium_purple",
        padding=(1, 2)
    )
    console.print(panel)

def get_download_option_v2(video_data):

    options = []
    if video_data.get("nwm_video_url"):
        options.append({"name": "Video (Tanpa Watermark)", "url": video_data.get("nwm_video_url"), "ext": ".mp4"})
    if video_data.get("nwm_video_url_HQ"):
        options.append({"name": "Video (Tanpa Watermark, HQ)", "url": video_data.get("nwm_video_url_HQ"), "ext": ".mp4"})
    if video_data.get("wm_video_url"):
        options.append({"name": "Video (Dengan Watermark)", "url": video_data.get("wm_video_url"), "ext": ".mp4"})
    if video_data.get("wm_video_url_HQ"):
        options.append({"name": "Video (Dengan Watermark, HQ)", "url": video_data.get("wm_video_url_HQ"), "ext": ".mp4"})

    music_data = video_data.get("music", {})
    if music_data and music_data.get("play_url") and music_data["play_url"].get("url_list"):
        options.append({"name": "Audio Only", "url": music_data["play_url"]["url_list"][0], "ext": ".mp3"})

    if not options:
        console.print("[bold red]Tidak ada opsi unduhan yang tersedia.[/bold red]")
        return None

    table = Table(
        show_header=True,
        header_style="bold cyan",
        title="[bold magenta]🎬 Pilih Media yang Akan Diunduh 🎬[/bold magenta]",
        title_style="bold magenta",
        title_justify="center",
        box=SQUARE, 
        show_lines=True,
        expand=True,
        padding=(0, 1)
    )
    table.add_column("No.", style="bold cyan", width=4, justify="center")
    table.add_column("Opsi", style="bold cyan", min_width=30)
    
    for i, option in enumerate(options):
        table.add_row(str(i + 1), option['name'])
    
    table.add_row("0", "[bold yellow]← Kembali[/bold yellow]")

    panel = Panel(
        table,
        border_style="medium_purple",
        padding=(1, 1)
    )
    console.print(panel)
    
    console.print("[dim]Pilih media yang ingin diunduh.[/dim]")
    console.print("[dim]Gunakan '0' atau 'b' untuk kembali.[/dim]")

    choice = cyber_input("Masukkan nomor pilihan")
    
    if choice in ['0', 'b']:
        return 'back' 
    
    if choice.isdigit() and 1 <= int(choice) <= len(options):
        return options[int(choice) - 1] 
    
    return 'invalid' 

def tiktok_downloader_v2():

    clear()
    print_cyber_panel("TikTok Downloader (v2)", "Unduh video/audio dari TikTok dengan API v2")
    
    url_input = cyber_input("URL TikTok (contoh: https://vt.tiktok.com/...) atau ketik '00' untuk kembali")
    
    if url_input == '00':
        return

    try:
        with console.status("[bold green]Mengambil informasi video...[/bold green]", spinner="dots"):
            config = load_config()
            if not config or not config.get("base_url"):
                console.print("[bold red]Error: Konfigurasi atau base_url tidak ditemukan.[/bold red]")
                cyber_input("Tekan Enter untuk kembali...")
                return

            api_endpoint = f"{config.get('base_url')}/api/downloader/v2/ttdl"
            encoded_url = quote(url_input)
            
            response = requests.get(f"{api_endpoint}?url={encoded_url}")
            response.raise_for_status()
            result = response.json()

        if result.get("success") and result.get("data"):
            data = result["data"]
            video_data = data.get("video_data", {})

            display_video_info_v2(data)

            selected_option = None
            while True:
                choice_result = get_download_option_v2(video_data)

                if choice_result == 'back':
                    return 
                elif choice_result == 'invalid':
                    console.print("[bold red]Pilihan tidak valid![/bold red]")
                    cyber_input("Tekan Enter untuk mencoba lagi...")
                    continue
                else:
                    selected_option = choice_result
                    break
            
            download_url = selected_option.get("url")
            extension = selected_option.get("ext")

            author_name = data.get("author", {}).get('nickname', 'tiktok_video')
            safe_title = "".join(c for c in data.get('desc', 'video') if c.isalnum() or c in (' ', '-', '_')).rstrip()
            filename = f"{author_name}_{safe_title}{extension}"

            output_path = get_output_path("downloads", filename)

            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
            }

            with console.status("[bold green]Mengunduh media...[/bold green]", spinner="dots"):
                media_response = requests.get(download_url, stream=True, headers=headers)
                media_response.raise_for_status()
                
                with open(output_path, 'wb') as f:
                    for chunk in media_response.iter_content(chunk_size=8192):
                        f.write(chunk)
            
            console.print(f"\n[bold green]✓ Media berhasil diunduh![/bold green]")
            console.print(f"[bold cyan]Lokasi:[/bold cyan] {output_path}")

            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            log_filename = f"tiktok_v2_download_log_{timestamp}.json"
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