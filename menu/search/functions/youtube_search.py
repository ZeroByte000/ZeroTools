import requests
import os
import json
from datetime import datetime
from urllib.parse import quote
from core.utils import load_config, get_output_path
from app.console import console, print_cyber_panel, cyber_input, clear
from rich.table import Table
from rich.panel import Panel
from rich.box import SQUARE
from rich.text import Text
from rich.console import Group

def display_youtube_info(data):
    clear()
    info_items = []
    
    title = data.get("title", "Unknown Title")
    url = data.get("url", "")
    description = data.get("description", "No description available")
    duration = data.get("duration", {})
    views = data.get("views", 0)
    author = data.get("author", {})
    thumbnail = data.get("thumbnail", "")
    
    info_items.append(Text.assemble(("Judul: ", "bold #00F0FF"), (title, "white")))
    
    if duration:
        timestamp = duration.get("timestamp", "Unknown")
        info_items.append(Text.assemble(("Durasi: ", "bold #00F0FF"), (timestamp, "white")))
    
    if views > 0:
        info_items.append(Text.assemble(("Views: ", "bold #00F0FF"), (f"{views:,}", "white")))
    
    if author:
        author_name = author.get("name", "Unknown Author")
        author_url = author.get("url", "")
        if author_url:
            info_items.append(Text.assemble(("Channel: ", "bold #00F0FF"), (author_name, "link cyan"), (f" ({author_url})", "dim")))
        else:
            info_items.append(Text.assemble(("Channel: ", "bold #00F0FF"), (author_name, "white")))
    
    if description:
        desc = description[:100] + "..." if len(description) > 100 else description
        info_items.append(Text.assemble(("Deskripsi: ", "bold #00F0FF"), (desc, "white")))
    
    if url:
        info_items.append(Text.assemble(("URL: ", "bold #00F0FF"), (url, "link cyan")))
    
    if thumbnail:
        info_items.append(Text.assemble(("Thumbnail: ", "bold #00F0FF"), (thumbnail, "link cyan")))
    
    info_group = Group(*info_items)
    
    panel = Panel(
        info_group,
        title="[bold magenta]🎬 Informasi Video YouTube 🎬[/bold magenta]",
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
            return None
        
        if choice.isdigit() and 1 <= int(choice) <= len(quality_options):
            return quality_options[int(choice) - 1]['value']
        
        console.print("[bold red]Pilihan tidak valid![/bold red]")
        cyber_input("Tekan Enter untuk mencoba lagi...")

def download_youtube_mp4(video_url, title):
    quality = get_video_quality()
    if quality is None:
        return False

    try:
        with console.status("[bold green]Mengambil informasi video...[/bold green]", spinner="dots"):
            config = load_config()
            if not config or not config.get("base_url"):
                console.print("[bold red]Error: Konfigurasi atau base_url tidak ditemukan.[/bold red]")
                cyber_input("Tekan Enter untuk kembali...")
                return False

            base_url = config.get("base_url")
            api_endpoint = f"{base_url}/api/downloader/ytmp4"

            encoded_url = quote(video_url)
            
            response = requests.get(f"{api_endpoint}?url={encoded_url}&quality={quality}")
            response.raise_for_status()
            result = response.json()

        if result.get("title"):
            display_downloaded_video_info(result)
            
            download_url = result.get("url", "")
            video_quality = result.get("quality", "Unknown")
            
            if not download_url:
                console.print("[bold red]URL unduhan tidak tersedia untuk kualitas ini.[/bold red]")
                cyber_input("Tekan Enter untuk kembali...")
                return False

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
            return True
        else:
            console.print(f"[bold red]Gagal mengambil informasi video.[/bold red]")
            console.print(f"Detail dari server: {result}")
            return False

    except requests.exceptions.RequestException as e:
        console.print(f"\n[bold red]Error saat menghubungi API:[/bold red] {e}")
        return False
    except Exception as e:
        console.print(f"\n[bold red]Terjadi kesalahan tak terduga:[/bold red] {e}")
        return False

def download_youtube_mp3(video_url, title):
    try:
        with console.status("[bold green]Mengambil informasi video...[/bold green]", spinner="dots"):
            config = load_config()
            if not config or not config.get("base_url"):
                console.print("[bold red]Error: Konfigurasi atau base_url tidak ditemukan.[/bold red]")
                cyber_input("Tekan Enter untuk kembali...")
                return False

            base_url = config.get("base_url")
            api_endpoint = f"{base_url}/api/downloader/ytmp3"
            
            encoded_url = quote(video_url)
            
            response = requests.get(f"{api_endpoint}?url={encoded_url}")
            response.raise_for_status()
            result = response.json()

        if result.get("title"):
            display_downloaded_audio_info(result)
            
            download_url = result.get("url", "")
            
            if not download_url:
                console.print("[bold red]URL unduhan tidak tersedia.[/bold red]")
                cyber_input("Tekan Enter untuk kembali...")
                return False
            
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
            return True
        else:
            console.print(f"[bold red]Gagal mengambil informasi video.[/bold red]")
            console.print(f"Detail dari server: {result}")
            return False

    except requests.exceptions.RequestException as e:
        console.print(f"\n[bold red]Error saat menghubungi API:[/bold red] {e}")
        return False
    except Exception as e:
        console.print(f"\n[bold red]Terjadi kesalahan tak terduga:[/bold red] {e}")
        return False

def display_downloaded_video_info(data):
    clear()
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

def display_downloaded_audio_info(data):
    clear()
    info_items = []
    
    title = data.get("title", "Unknown Title")
    author = data.get("author", "Unknown Author")
    author_url = data.get("authorUrl", "")
    length_seconds = data.get("lengthSeconds", 0)
    views = data.get("views", 0)
    upload_date = data.get("uploadDate", "Unknown")
    thumbnail = data.get("thumbnail", "")
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
        title="[bold magenta]🎵 Informasi Audio 🎵[/bold magenta]",
        border_style="medium_purple",
        padding=(1, 2)
    )
    console.print(panel)

def display_videos_with_options(videos, page=1, items_per_page=5):
    clear()
    

    total_videos = len(videos)
    total_pages = (total_videos + items_per_page - 1) // items_per_page  
    start_index = (page - 1) * items_per_page
    end_index = min(start_index + items_per_page, total_videos)
    current_videos = videos[start_index:end_index]
    
    console.print(f"[bold green]Daftar Video YouTube (Halaman {page}/{total_pages}):[/bold green]")
    
    for i, video in enumerate(current_videos, start_index + 1):
        title = video.get("title", "Unknown Title")
        author = video.get("author", {}).get("name", "Unknown Author")
        duration = video.get("duration", {}).get("timestamp", "Unknown")
        views = video.get("views", 0)
        
        video_info = Text.assemble(
            (f"{i}. ", "bold cyan"),
            (title, "bold white"),
            ("\n   Channel: ", "cyan"),
            (author, "white"),
            ("\n   Durasi: ", "cyan"),
            (duration, "white"),
            ("\n   Views: ", "cyan"),
            (f"{views:,}" if views > 0 else "N/A", "white")
        )
        
        panel = Panel(
            video_info,
            border_style="medium_purple",
            padding=(0, 1)
        )
        console.print(panel)
    
    pagination_info = Text.assemble(
        ("Menampilkan ", "dim"),
        (f"{start_index + 1}-{end_index}", "bold cyan"),
        (" dari ", "dim"),
        (f"{total_videos}", "bold cyan"),
        (" video", "dim")
    )
    console.print(pagination_info)
    
    console.print("\n[bold cyan]Pilihan:[/bold cyan]")
    console.print("[bold cyan]1-[/bold cyan][white] Pilih nomor video untuk melihat detail[/white]")
    console.print("[bold cyan]M[/bold cyan][white] Unduh MP3 (Audio)[/white]")
    console.print("[bold cyan]V[/bold cyan][white] Unduh MP4 (Video)[/white]")
    console.print("[bold cyan]P[/bold cyan][white] Halaman Sebelumnya[/white]")
    console.print("[bold cyan]N[/bold cyan][white] Halaman Berikutnya[/white]")
    console.print("[bold cyan]G[/bold cyan][white] Go to Page (Pergi ke halaman)[/white]")
    console.print("[bold cyan]00[/bold cyan][white] Kembali ke pencarian[/white]")
    
    while True:
        choice = cyber_input("Masukkan pilihan: ")
        
        if choice == '00':
            return 'back'
        elif choice.upper() == 'P':
            if page > 1:
                return {'action': 'page', 'page': page - 1}
            else:
                console.print("[red]Anda sudah di halaman pertama.[/red]")
                cyber_input("Tekan Enter untuk melanjutkan...")
        elif choice.upper() == 'N':
            if page < total_pages:
                return {'action': 'page', 'page': page + 1}
            else:
                console.print("[red]Anda sudah di halaman terakhir.[/red]")
                cyber_input("Tekan Enter untuk melanjutkan...")
        elif choice.upper() == 'G':
            page_input = cyber_input(f"Masukkan nomor halaman (1-{total_pages}): ")
            try:
                page_num = int(page_input)
                if 1 <= page_num <= total_pages:
                    return {'action': 'page', 'page': page_num}
                else:
                    console.print(f"[red]Nomor halaman harus antara 1 dan {total_pages}.[/red]")
                    cyber_input("Tekan Enter untuk melanjutkan...")
            except ValueError:
                console.print("[red]Input tidak valid. Masukkan nomor halaman.[/red]")
                cyber_input("Tekan Enter untuk melanjutkan...")
        elif choice.upper() == 'M':
            video_choice = cyber_input("Pilih nomor video untuk diunduh sebagai MP3: ")
            try:
                video_index = int(video_choice) - 1
                if 0 <= video_index < total_videos:
                    selected_video = videos[video_index]
                    video_url = selected_video.get("url", "")
                    title = selected_video.get("title", "Unknown Title")
                    if video_url:
                        if download_youtube_mp3(video_url, title):
                            cyber_input("Tekan Enter untuk melanjutkan...")
                            return 'downloaded'
                    else:
                        console.print("[red]URL video tidak tersedia.[/red]")
                        cyber_input("Tekan Enter untuk melanjutkan...")
                else:
                    console.print("[red]Nomor video tidak valid.[/red]")
                    cyber_input("Tekan Enter untuk melanjutkan...")
            except ValueError:
                console.print("[red]Input tidak valid. Masukkan nomor video.[/red]")
                cyber_input("Tekan Enter untuk melanjutkan...")
        elif choice.upper() == 'V':
            video_choice = cyber_input("Pilih nomor video untuk diunduh sebagai MP4: ")
            try:
                video_index = int(video_choice) - 1
                if 0 <= video_index < total_videos:
                    selected_video = videos[video_index]
                    video_url = selected_video.get("url", "")
                    title = selected_video.get("title", "Unknown Title")
                    if video_url:
                        if download_youtube_mp4(video_url, title):
                            cyber_input("Tekan Enter untuk melanjutkan...")
                            return 'downloaded'
                    else:
                        console.print("[red]URL video tidak tersedia.[/red]")
                        cyber_input("Tekan Enter untuk melanjutkan...")
                else:
                    console.print("[red]Nomor video tidak valid.[/red]")
                    cyber_input("Tekan Enter untuk melanjutkan...")
            except ValueError:
                console.print("[red]Input tidak valid. Masukkan nomor video.[/red]")
                cyber_input("Tekan Enter untuk melanjutkan...")
        else:
            try:
                video_index = int(choice) - 1
                if 0 <= video_index < total_videos:
                    selected_video = videos[video_index]
                    display_youtube_info(selected_video)
                    
                    console.print("\n[bold cyan]Pilihan:[/bold cyan]")
                    console.print("[bold cyan]M[/bold cyan][white] Unduh MP3 (Audio)[/white]")
                    console.print("[bold cyan]V[/bold cyan][white] Unduh MP4 (Video)[/white]")
                    console.print("[bold cyan]00[/bold cyan][white] Kembali ke daftar video[/white]")
                    
                    download_choice = cyber_input("Masukkan pilihan: ")
                    
                    if download_choice == '00':
                        return {'action': 'page', 'page': page}
                    elif download_choice.upper() == 'M':
                        video_url = selected_video.get("url", "")
                        title = selected_video.get("title", "Unknown Title")
                        if video_url:
                            if download_youtube_mp3(video_url, title):
                                cyber_input("Tekan Enter untuk melanjutkan...")
                                return 'downloaded'
                        else:
                            console.print("[red]URL video tidak tersedia.[/red]")
                            cyber_input("Tekan Enter untuk melanjutkan...")
                    elif download_choice.upper() == 'V':
                        video_url = selected_video.get("url", "")
                        title = selected_video.get("title", "Unknown Title")
                        if video_url:
                            if download_youtube_mp4(video_url, title):
                                cyber_input("Tekan Enter untuk melanjutkan...")
                                return 'downloaded'
                        else:
                            console.print("[red]URL video tidak tersedia.[/red]")
                            cyber_input("Tekan Enter untuk melanjutkan...")
                    else:
                        console.print("[red]Pilihan tidak valid.[/red]")
                        cyber_input("Tekan Enter untuk melanjutkan...")
                else:
                    console.print("[red]Nomor video tidak valid.[/red]")
                    cyber_input("Tekan Enter untuk melanjutkan...")
            except ValueError:
                console.print("[red]Input tidak valid. Masukkan nomor video, M, V, P, N, G, atau 00.[/red]")
                cyber_input("Tekan Enter untuk melanjutkan...")

def youtube_search():
    clear()
    print_cyber_panel("YouTube Search", "Cari video di platform YouTube.")
    
    config = load_config()
    if not config or not config.get("base_url"):
        console.print("[bold red]Error: Konfigurasi atau base_url tidak ditemukan.[/bold red]")
        cyber_input("Tekan Enter untuk kembali...")
        return

    search_api_endpoint = f"{config.get('base_url')}/api/search/yt"
    
    while True:
        query = cyber_input("Masukkan kata kunci pencarian atau ketik '00' untuk kembali")
        
        if query == '00':
            return

        try:
            with console.status("[bold green]Mencari di YouTube...[/bold green]", spinner="dots"):
                params = {'query': query}
                response = requests.get(search_api_endpoint, params=params, headers={'accept': 'application/json'})
                response.raise_for_status()
                search_result = response.json()

            if search_result and "videos" in search_result:
                videos = search_result.get("videos", [])
                total = search_result.get("total", 0)
                
                if videos:
                    console.print(f"\n[bold green]Ditemukan {total} video:[/bold green]")
                    
                    current_page = 1
                    items_per_page = 5
                    
                    while True:
                        result = display_videos_with_options(videos, current_page, items_per_page)
                        
                        if result == 'back':
                            break
                        elif result == 'downloaded':
                            continue
                        elif isinstance(result, dict) and result.get('action') == 'page':
                            current_page = result.get('page', 1)
                            continue
                else:
                    console.print("[bold red]Tidak ada video yang ditemukan.[/bold red]")
            else:
                console.print("[bold red]Tidak ada hasil yang ditemukan.[/bold red]")
            
        except requests.exceptions.RequestException as e:
            console.print(f"\n[bold red]Error saat menghubungi API:[/bold red] {e}")
        except Exception as e:
            console.print(f"\n[bold red]Terjadi kesalahan tak terduga:[/bold red] {e}")
        
        cyber_input("\nTekan Enter untuk kembali ke menu Search...")