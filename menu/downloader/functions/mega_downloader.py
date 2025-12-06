# menu/downloader/functions/mega_downloader.py

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

def format_filesize(size_in_bytes):

    if size_in_bytes < 1024 * 1024:
        return f"{size_in_bytes / 1024:.2f} KB"
    elif size_in_bytes < 1024 * 1024 * 1024:
        return f"{size_in_bytes / (1024 * 1024):.2f} MB"
    else:
        return f"{size_in_bytes / (1024 * 1024 * 1024):.2f} GB"

def display_mega_info(file_info):

    info_items = []
    
    filename = file_info.get("name", "file")
    title = file_info.get("title", "N/A")
    size_in_bytes = file_info.get("size", 0)
    
    info_items.append(Text.assemble(("Nama File: ", "bold cyan"), (filename, "white")))
    info_items.append(Text.assemble(("Title: ", "bold cyan"), (title, "white")))
    info_items.append(Text.assemble(("Ukuran: ", "bold cyan"), (format_filesize(size_in_bytes), "white")))
    
    info_group = Group(*info_items)
    
    panel = Panel(
        info_group,
        title="[bold magenta]📄 Informasi File 📄[/bold magenta]",
        border_style="medium_purple",
        padding=(1, 2)
    )
    console.print(panel)

def mega_downloader():

    clear()
    print_cyber_panel("Mega Downloader", "Unduh file dari Mega.nz")
    
    url_input = cyber_input("URL Mega.nz (contoh: https://mega.nz/file/...) atau ketik '00' untuk kembali")
    
    if url_input == '00':
        return

    try:
        with console.status("[bold green]Mengambil informasi file...[/bold green]", spinner="dots"):
            config = load_config()
            if not config or not config.get("base_url"):
                console.print("[bold red]Error: Konfigurasi atau base_url tidak ditemukan.[/bold red]")
                cyber_input("Tekan Enter untuk kembali...")
                return

            base_url = config.get("base_url")
            api_endpoint = f"{base_url}/api/downloader/mega"
            
            encoded_url = quote(url_input)
            
            response = requests.get(f"{api_endpoint}?url={encoded_url}")
            response.raise_for_status()
            result = response.json()

        file_list = result.get("result", [])

        if not file_list:
            console.print("[bold red]Tidak ada file yang ditemukan di URL tersebut.[/bold red]")
            cyber_input("Tekan Enter untuk kembali...")
            return

        file_info = file_list[0]

        display_mega_info(file_info)
        
        download_url = file_info.get("link", "")
        filename = file_info.get("name", "file")
        
        if not download_url:
            console.print("[bold red]URL unduhan tidak tersedia.[/bold red]")
            cyber_input("Tekan Enter untuk kembali...")
            return

        output_path = get_output_path("downloads", filename)

        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }

        try:
            with console.status("[bold green]Mengunduh file...[/bold green]", spinner="dots"):
                file_response = requests.get(download_url, stream=True, headers=headers)
                file_response.raise_for_status()
                
                with open(output_path, 'wb') as f:
                    for chunk in file_response.iter_content(chunk_size=8192):
                        f.write(chunk)
            
            console.print(f"\n[bold green]✓ File berhasil diunduh![/bold green]")
            console.print(f"[bold cyan]Lokasi:[/bold cyan] {output_path}")

            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            log_filename = f"mega_download_log_{timestamp}.json"
            log_path = get_output_path("output", log_filename, no_prompt=True)
            
            with open(log_path, 'w') as f:
                json.dump(result, f, indent=4)
            
            console.print(f"[dim]Log respons disimpan di: {log_path}[/dim]")
        except requests.exceptions.RequestException as e:
            console.print(f"[bold red]Gagal mengunduh '{filename}': {e}[/bold red]")
        
    except requests.exceptions.RequestException as e:
        console.print(f"\n[bold red]Error saat menghubungi API:[/bold red] {e}")
    except Exception as e:
        console.print(f"\n[bold red]Terjadi kesalahan tak terduga:[/bold red] {e}")
        
    cyber_input("\nTekan Enter untuk kembali ke menu...")