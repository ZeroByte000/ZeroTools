import requests
import os
from datetime import datetime
from core.utils import load_config, get_output_path
from app.console import console, print_cyber_panel, cyber_input, clear
from rich.panel import Panel
from rich.text import Text
from rich.console import Group
from rich.align import Align
from rich.table import Table
from rich.box import SQUARE

def display_wallpaper_list(wallpapers, query, page=1, per_page=5):
    """Menampilkan daftar wallpaper dengan pagination."""
    clear()
    if not wallpapers:
        console.print("[bold red]Tidak ada wallpaper yang ditemukan.[/bold red]")
        cyber_input("Tekan Enter untuk kembali...")
        return None, page

    total_pages = (len(wallpapers) + per_page - 1) // per_page
    
    start_index = (page - 1) * per_page
    end_index = min(start_index + per_page, len(wallpapers))
    current_page_data = wallpapers[start_index:end_index]
    
    wallpaper_panels = []
    
    for i, wallpaper in enumerate(current_page_data, start=start_index + 1):
        wp_content = [
            Text.assemble((f"{i}. ", "bold cyan")),
            Text.assemble(("Judul: ", "bold #00F0FF"), (wallpaper.get('title', 'N/A'), "white")),
            Text.assemble(("Wallpaper: ", "bold #00F0FF"), (wallpaper.get('wallpaper', 'N/A'), "white")),
        ]
        
        wp_panel = Panel(
            Group(*wp_content),
            title=f"[bold white]Wallpaper {i}[/bold white]",
            border_style="medium_purple",
            padding=(0, 1)
        )
        wallpaper_panels.append(wp_panel)

    pagination_info = Text.assemble(
        (f"Halaman {page} dari {total_pages} ", "bold cyan"),
        (f"({len(wallpapers)} total)", "dim")
    )
    
    console.print(Panel(
        Group(*wallpaper_panels),
        title=f"[bold magenta]🖼️ Hasil Pencarian untuk '{query}' 🖼️[/bold magenta]",
        subtitle=pagination_info,
        border_style="#00F0FF",
        padding=(1, 1)
    ))
    
    console.print("\n[bold cyan]Navigasi:[/bold cyan]")
    
    navigation_table = Table(show_header=False, box=None, padding=0)
    navigation_table.add_column("Pilihan", style="bold cyan", width=15)
    navigation_table.add_column("Deskripsi", style="white")
    
    navigation_table.add_row("No", "Pilih nomor wallpaper")
    
    if page > 1:
        navigation_table.add_row("P", f"Halaman sebelumnya ({page-1})")
    
    if page < total_pages:
        navigation_table.add_row("N", f"Halaman berikutnya ({page+1})")
    
    navigation_table.add_row("00", "Kembali ke pencarian")
    
    console.print(navigation_table)
    
    while True:
        choice = cyber_input("Masukkan pilihan: ")
        
        if choice == '00':
            return None, page

        elif choice.upper() == 'P' and page > 1:
            return 'prev_page', page - 1
        elif choice.upper() == 'N' and page < total_pages:
            return 'next_page', page + 1

        else:
            try:

                wallpaper_index = int(choice) - 1

                global_index = start_index + wallpaper_index
                
                if 0 <= global_index < len(wallpapers):
                    selected_wallpaper = wallpapers[global_index]
                    return selected_wallpaper, page
                else:
                    console.print("[red]Nomor wallpaper tidak valid.[/red]")
                    cyber_input("Tekan Enter untuk melanjutkan...")
            except ValueError:
                console.print("[red]Input tidak valid. Masukkan nomor wallpaper, P, N, atau 00.[/red]")
                cyber_input("Tekan Enter untuk melanjutkan...")

def download_wallpaper(wallpaper_data, page):
    """Mengunduh wallpaper."""
    wallpaper_url_to_download = wallpaper_data.get('wallpaper')

    if not wallpaper_url_to_download:
        console.print("[bold red]Link wallpaper tidak ditemukan.[/bold red]")
        cyber_input("Tekan Enter untuk melanjutkan...")
        return 'back_to_list'

    last_dash_index = wallpaper_url_to_download.rfind('-')
    if last_dash_index != -1:
        clean_url = wallpaper_url_to_download[:last_dash_index] + ".jpg"
    else:
        clean_url = wallpaper_url_to_download

    safe_title = "".join(c for c in wallpaper_data.get('title', 'wallpaper') if c.isalnum() or c in (' ', '-', '_')).rstrip()
    filename = f"wallpaper_{safe_title}.jpg"
    
    output_path = get_output_path("downloads", filename)
    
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }

    try:
        with console.status("[bold green]Mengunduh wallpaper...[/bold green]", spinner="dots"):
            image_response = requests.get(clean_url, stream=True, headers=headers)
            image_response.raise_for_status()
            
            with open(output_path, 'wb') as f:
                for chunk in image_response.iter_content(chunk_size=8192):
                    f.write(chunk)
        
        console.print(f"\n[bold green]✓ Wallpaper berhasil diunduh![/bold green]")
        console.print(f"[bold cyan]Lokasi:[/bold cyan] {output_path}")
        cyber_input("Tekan Enter untuk kembali ke daftar...")
        return 'back_to_list'
    except requests.exceptions.RequestException as e:
        console.print(f"\n[bold red]Gagal mengunduh wallpaper: {e}[/bold red]")
        cyber_input("Tekan Enter untuk melanjutkan...")
        return 'back_to_list'

def wallpaper_search():
    """Mencari dan mengunduh wallpaper anime."""
    clear()
    print_cyber_panel("Wallpaper Search", "Cari dan unduh wallpaper anime.")
    
    config = load_config()
    if not config or not config.get("base_url"):
        console.print("[bold red]Error: Konfigurasi atau base_url tidak ditemukan.[/bold red]")
        cyber_input("Tekan Enter untuk kembali...")
        return

    search_api_endpoint = f"{config.get('base_url')}/api/search/wallpaper-moe"
    
    while True:
        query = cyber_input("Masukkan kata kunci pencarian atau ketik '00' untuk kembali")
        
        if query == '00':
            return

        try:
            with console.status("[bold green]Mencari wallpaper...[/bold green]", spinner="dots"):
                params = {'query': query}
                response = requests.get(search_api_endpoint, params=params, headers={'accept': 'application/json'})
                response.raise_for_status()
                search_result = response.json()

            if not (search_result.get("success") and search_result.get("result")):
                console.print("[bold red]Tidak ada hasil yang ditemukan.[/bold red]")
                cyber_input("Tekan Enter untuk mencari lagi...")
                continue

            wallpapers = search_result.get("result", [])

            current_page = 1
            per_page = 5  
            
            while True:
                result_action, new_page = display_wallpaper_list(wallpapers, query, current_page, per_page)
                
                if result_action is None:
                    break  
                elif result_action == 'prev_page':
                    current_page = new_page
                elif result_action == 'next_page':
                    current_page = new_page
                else:

                    action_result = download_wallpaper(result_action, current_page)
                    
                    if action_result == 'back_to_list':
                        continue

        except requests.exceptions.RequestException as e:
            console.print(f"\n[bold red]Error saat menghubungi API:[/bold red] {e}")
        except Exception as e:
            console.print(f"\n[bold red]Terjadi kesalahan tak terduga:[/bold red] {e}")
        
        cyber_input("\nTekan Enter untuk kembali ke menu Search...")