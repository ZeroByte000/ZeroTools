# menu/downloader/functions/threads_downloader.py

import os
import requests
import json
from urllib.parse import quote
from datetime import datetime
from core.utils import load_config, get_output_path
from app.console import console, print_cyber_panel, cyber_input, clear

def threads_downloader():

    clear()
    print_cyber_panel("Threads Downloader", "Unduh media (gambar/video) dari Threads")

    url_input = cyber_input("URL Threads (contoh: https://www.threads.com/...) atau ketik '00' untuk kembali")

    if url_input == '00':
        return

    try:
        with console.status("[bold green]Mengambil informasi media...[/bold green]", spinner="dots"):
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

            api_endpoint = f"{base_url}/api/downloader/threads"

            encoded_url = quote(url_input)
            
            response = requests.get(f"{api_endpoint}?url={encoded_url}")
            response.raise_for_status()
            result = response.json()

        image_urls = result.get("image_urls", [])
        video_urls = result.get("video_urls", [])
        all_media_urls = image_urls + video_urls

        if not all_media_urls:
            console.print("[bold red]Tidak ada media yang ditemukan di URL tersebut.[/bold red]")
            cyber_input("Tekan Enter untuk kembali...")
            return
        
        console.print(f"\n[bold green]✓ Ditemukan {len(all_media_urls)} media.[/bold green]")

        post_timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        post_folder_name = f"threads_post_{post_timestamp}"
        
        dummy_path = get_output_path("downloads", "dummy.txt")
        downloads_dir = os.path.dirname(dummy_path)
        post_dir = os.path.join(downloads_dir, post_folder_name)
        os.makedirs(post_dir, exist_ok=True)

        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }

        downloaded_count = 0
        with console.status("[bold green]Mengunduh media...[/bold green]", spinner="dots"):
            for i, media_url in enumerate(all_media_urls):
                try:

                    if ".jpg" in media_url:
                        ext = ".jpg"
                    elif ".mp4" in media_url:
                        ext = ".mp4"
                    else:
                        ext = "" 
                    
                    filename = f"media_{i+1}{ext}"
                    output_path = os.path.join(post_dir, filename)

                    media_response = requests.get(media_url, stream=True, headers=headers)
                    media_response.raise_for_status()
                    
                    with open(output_path, 'wb') as f:
                        for chunk in media_response.iter_content(chunk_size=8192):
                            f.write(chunk)
                    downloaded_count += 1
                except requests.exceptions.RequestException:
                    console.print(f"[yellow]Gagal mengunduh media ke-{i+1}. Melewati.[/yellow]")
        
        console.print(f"\n[bold green]✓ Berhasil mengunduh {downloaded_count} media![/bold green]")
        console.print(f"[bold cyan]Lokasi:[/bold cyan] {post_dir}")

        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        log_filename = f"threads_download_log_{timestamp}.json"
        log_path = get_output_path("output", log_filename, no_prompt=True)
        
        with open(log_path, 'w') as f:
            json.dump(result, f, indent=4)
        
        console.print(f"[dim]Log respons disimpan di: {log_path}[/dim]")

    except requests.exceptions.RequestException as e:
        console.print(f"\n[bold red]Error saat menghubungi API:[/bold red] {e}")
    except Exception as e:
        console.print(f"\n[bold red]Terjadi kesalahan tak terduga:[/bold red] {e}")
        
    cyber_input("\nTekan Enter untuk kembali ke menu...")