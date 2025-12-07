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

def display_image_info(data):
    clear()
    info_items = []
    
    title = data.get("title", "Unknown Title")
    url = data.get("url", "")
    image_url = data.get("image", "")
    
    info_items.append(Text.assemble(("Judul: ", "bold #00F0FF"), (title, "white")))
    
    if url:
        info_items.append(Text.assemble(("URL: ", "bold #00F0FF"), (url, "link cyan")))
    
    if image_url:
        info_items.append(Text.assemble(("URL Gambar: ", "bold #00F0FF"), (image_url, "link cyan")))
    
    info_group = Group(*info_items)
    
    panel = Panel(
        info_group,
        title="[bold magenta]🖼️ Informasi Gambar Google 🖼️[/bold magenta]",
        border_style="medium_purple",
        padding=(1, 2)
    )
    console.print(panel)

def download_image(image_url, title):
    try:
        with console.status("[bold green]Mengunduh gambar...[/bold green]", spinner="dots"):
            if not image_url:
                console.print("[bold red]URL gambar tidak tersedia.[/bold red]")
                return False
            
            safe_title = "".join(c for c in title if c.isalnum() or c in (' ', '-', '_')).rstrip()
            filename = f"{safe_title}.jpg"
            
            output_path = get_output_path("downloads", filename)
            
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
            }
            
            response = requests.get(image_url, stream=True, headers=headers)
            response.raise_for_status()
            
            with open(output_path, 'wb') as f:
                for chunk in response.iter_content(chunk_size=8192):
                    f.write(chunk)
        
        console.print(f"\n[bold green]✓ Gambar berhasil diunduh![/bold green]")
        console.print(f"[bold cyan]Lokasi:[/bold cyan] {output_path}")
        
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        log_filename = f"google_image_download_log_{timestamp}.json"
        log_path = get_output_path("output", log_filename, no_prompt=True)
        
        with open(log_path, 'w') as f:
            json.dump({"title": title, "url": image_url, "saved_at": output_path}, f, indent=4)
        
        console.print(f"[dim]Log respons disimpan di: {log_path}[/dim]")
        return True
    except requests.exceptions.RequestException as e:
        console.print(f"\n[bold red]Error saat mengunduh gambar:[/bold red] {e}")
        return False
    except Exception as e:
        console.print(f"\n[bold red]Terjadi kesalahan tak terduga:[/bold red] {e}")
        return False

def display_images_with_options(images):
    clear()
    console.print("[bold green]Daftar Gambar Google:[/bold green]")
    
    for i, image in enumerate(images, 1):
        title = image.get("title", "Unknown Title")
        url = image.get("url", "")
        
        image_info = Text.assemble(
            (f"{i}. ", "bold cyan"),
            (title[:50] + "..." if len(title) > 50 else title, "bold white"),
            ("\n   URL: ", "cyan"),
            (url[:50] + "..." if len(url) > 50 else url, "white")
        )
        
        panel = Panel(
            image_info,
            border_style="medium_purple",
            padding=(0, 1)
        )
        console.print(panel)
    
    console.print("\n[bold cyan]Pilihan:[/bold cyan]")
    console.print("[bold cyan]1-[/bold cyan][white] Pilih nomor gambar untuk melihat detail[/white]")
    console.print("[bold cyan]D[/bold cyan][white] Unduh gambar langsung[/white]")
    console.print("[bold cyan]00[/bold cyan][white] Kembali ke pencarian[/white]")
    
    while True:
        choice = cyber_input("Masukkan pilihan: ")
        
        if choice == '00':
            return 'back'
        elif choice.upper() == 'D':
            image_choice = cyber_input("Pilih nomor gambar untuk diunduh: ")
            try:
                image_index = int(image_choice) - 1
                if 0 <= image_index < len(images):
                    selected_image = images[image_index]
                    image_url = selected_image.get("image", "")
                    title = selected_image.get("title", "Unknown Title")
                    if image_url:
                        if download_image(image_url, title):
                            cyber_input("Tekan Enter untuk melanjutkan...")
                            return 'downloaded'
                    else:
                        console.print("[red]URL gambar tidak tersedia.[/red]")
                        cyber_input("Tekan Enter untuk melanjutkan...")
                else:
                    console.print("[red]Nomor gambar tidak valid.[/red]")
                    cyber_input("Tekan Enter untuk melanjutkan...")
            except ValueError:
                console.print("[red]Input tidak valid. Masukkan nomor gambar.[/red]")
                cyber_input("Tekan Enter untuk melanjutkan...")
        else:
            try:
                image_index = int(choice) - 1
                if 0 <= image_index < len(images):
                    selected_image = images[image_index]
                    display_image_info(selected_image)
                    
                    console.print("\n[bold cyan] Pilihan:[/bold cyan]")
                    console.print("[bold cyan]D[/bold cyan][white] Unduh gambar[/white]")
                    console.print("[bold cyan]00[/bold cyan][white] Kembali ke daftar gambar[/white]")
                    
                    download_choice = cyber_input("Masukkan pilihan: ")
                    
                    if download_choice == '00':
                        return 'back_to_images'
                    elif download_choice.upper() == 'D':
                        image_url = selected_image.get("image", "")
                        title = selected_image.get("title", "Unknown Title")
                        if image_url:
                            if download_image(image_url, title):
                                cyber_input("Tekan Enter untuk melanjutkan...")
                                return 'downloaded'
                        else:
                            console.print("[red]URL gambar tidak tersedia.[/red]")
                            cyber_input("Tekan Enter untuk melanjutkan...")
                    else:
                        console.print("[red]Pilihan tidak valid.[/red]")
                        cyber_input("Tekan Enter untuk melanjutkan...")
                else:
                    console.print("[red]Nomor gambar tidak valid.[/red]")
                    cyber_input("Tekan Enter untuk melanjutkan...")
                    clear()
                    console.print("[bold green]Daftar Gambar Google:[/bold green]")
                    for i, image in enumerate(images, 1):
                        title = image.get("title", "Unknown Title")
                        url = image.get("url", "")
                        
                        image_info = Text.assemble(
                            (f"{i}. ", "bold cyan"),
                            (title[:50] + "..." if len(title) > 50 else title, "bold white"),
                            ("\n   URL: ", "cyan"),
                            (url[:50] + "..." if len(url) > 50 else url, "white")
                        )
                        
                        panel = Panel(
                            image_info,
                            border_style="medium_purple",
                            padding=(0, 1)
                        )
                        console.print(panel)
            except ValueError:
                console.print("[red]Input tidak valid. Masukkan nomor gambar, D, atau 00.[/red]")
                cyber_input("Tekan Enter untuk melanjutkan...")

def google_image_search():
    clear()
    print_cyber_panel("Google Image Search", "Cari gambar di Google.")
    
    config = load_config()
    if not config or not config.get("base_url"):
        console.print("[bold red]Error: Konfigurasi atau base_url tidak ditemukan.[/bold red]")
        cyber_input("Tekan Enter untuk kembali...")
        return

    search_api_endpoint = f"{config.get('base_url')}/api/search/gimage"
    
    while True:
        query = cyber_input("Masukkan kata kunci pencarian atau ketik '00' untuk kembali")
        
        if query == '00':
            return

        try:
            with console.status("[bold green]Mencari gambar di Google...[/bold green]", spinner="dots"):
                params = {'query': query}
                response = requests.get(search_api_endpoint, params=params, headers={'accept': 'application/json'})
                response.raise_for_status()
                search_result = response.json()

            if search_result and isinstance(search_result, list):
                images = search_result
                
                if images:
                    console.print(f"\n[bold green]Ditemukan {len(images)} gambar:[/bold green]")
                    result = display_images_with_options(images)
                    
                    if result == 'back':
                        continue
                    elif result == 'downloaded':
                        continue
                    elif result == 'back_to_images':
                        result = display_images_with_options(images)
                        
                        if result == 'back':
                            continue
                        elif result == 'downloaded':
                            continue
                else:
                    console.print("[bold red]Tidak ada gambar yang ditemukan.[/bold red]")
            else:
                console.print("[bold red]Tidak ada hasil yang ditemukan.[/bold red]")
            
        except requests.exceptions.RequestException as e:
            console.print(f"\n[bold red]Error saat menghubungi API:[/bold red] {e}")
        except Exception as e:
            console.print(f"\n[bold red]Terjadi kesalahan tak terduga:[/bold red] {e}")
        
        cyber_input("\nTekan Enter untuk kembali ke menu Search...")