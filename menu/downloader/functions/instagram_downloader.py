# menu/downloader/functions/instagram_downloader.py

import os
import requests
import json
from urllib.parse import quote
from datetime import datetime
from core.utils import load_config, get_output_path
from app.console import console, print_cyber_panel, cyber_input, clear

def instagram_downloader():
    clear()
    print_cyber_panel("Instagram Downloader", "Unduh media (gambar/video) dari Instagram")

    url_input = cyber_input("URL Instagram (contoh: https://www.instagram.com/p/...) atau ketik '00' untuk kembali")

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

            api_endpoint = f"{base_url}/api/downloader/igdl"
            
            encoded_url = quote(url_input)
            
            response = requests.get(f"{api_endpoint}?url={encoded_url}")
            response.raise_for_status()
            result = response.json()

        if result.get("status"):
            media_list = result.get("data", [])

            if not media_list:
                console.print("[bold red]Tidak ada media yang ditemukan di URL tersebut.[/bold red]")
                cyber_input("Tekan Enter untuk kembali...")
                return
            
            console.print(f"\n[bold green]✓ Ditemukan {len(media_list)} media.[/bold green]")

            post_timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            post_folder_name = f"instagram_post_{post_timestamp}"

            dummy_path = get_output_path("downloads", "dummy.txt")
            downloads_dir = os.path.dirname(dummy_path)
            post_dir = os.path.join(downloads_dir, post_folder_name)
            os.makedirs(post_dir, exist_ok=True)

            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
            }

            downloaded_count = 0
            with console.status("[bold green]Mengunduh media...[/bold green]", spinner="dots"):
                for i, media_item in enumerate(media_list):
                    try:
                        media_url = media_item.get("url")
                        media_type = media_item.get("type", "image")
                        
                        if not media_url:
                            continue

                        ext = ".jpg" if media_type == "image" else ".mp4"
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
            log_filename = f"instagram_download_log_{timestamp}.json"
            log_path = get_output_path("output", log_filename, no_prompt=True)
            
            with open(log_path, 'w') as f:
                json.dump(result, f, indent=4)
            
            console.print(f"[dim]Log respons disimpan di: {log_path}[/dim]")
        else:
            console.print(f"[bold red]Gagal mengambil informasi media.[/bold red]")
            console.print(f"Detail dari server: {result}")

    except requests.exceptions.RequestException as e:
        console.print(f"\n[bold red]Error saat menghubungi API:[/bold red] {e}")
    except Exception as e:
        console.print(f"\n[bold red]Terjadi kesalahan tak terduga:[/bold red] {e}")
        
    cyber_input("\nTekan Enter untuk kembali ke menu...")