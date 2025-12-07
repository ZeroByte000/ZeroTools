import requests
import os
import webbrowser
from datetime import datetime
from core.utils import load_config, get_output_path
from app.console import console, print_cyber_panel, cyber_input, clear
from rich.panel import Panel
from rich.text import Text
from rich.console import Group
from rich.align import Align
from rich.table import Table
from rich.box import SQUARE

def display_pinterest_list(images, query, page=1, per_page=5):
    """Menampilkan daftar gambar Pinterest dengan pagination."""
    clear()
    if not images:
        console.print("[bold red]Tidak ada gambar yang ditemukan.[/bold red]")
        cyber_input("Tekan Enter untuk kembali...")
        return None, page

    total_pages = (len(images) + per_page - 1) // per_page

    start_index = (page - 1) * per_page
    end_index = min(start_index + per_page, len(images))
    current_page_data = images[start_index:end_index]
    
    image_panels = []
    
    for i, image in enumerate(current_page_data, start=start_index + 1):
        image_content = [
            Text.assemble((f"{i}. ", "bold cyan")),
            Text.assemble(("Link Pinterest: ", "bold #00F0FF"), (image.get('link', 'N/A'), "link cyan")),
            Text.assemble(("Link Gambar: ", "bold #00F0FF"), (image.get('directLink', 'N/A'), "white")),
        ]
        
        image_panel = Panel(
            Group(*image_content),
            title=f"[bold white]Gambar {i}[/bold white]",
            border_style="medium_purple",
            padding=(0, 1)
        )
        image_panels.append(image_panel)

    pagination_info = Text.assemble(
        (f"Halaman {page} dari {total_pages} ", "bold cyan"),
        (f"({len(images)} total)", "dim")
    )
    
    console.print(Panel(
        Group(*image_panels),
        title=f"[bold magenta]📌 Hasil Pencarian untuk '{query}' 📌[/bold magenta]",
        subtitle=pagination_info,
        border_style="#00F0FF",
        padding=(1, 1)
    ))

    console.print("\n[bold cyan]Navigasi:[/bold cyan]")
    
    navigation_table = Table(show_header=False, box=None, padding=0)
    navigation_table.add_column("Pilihan", style="bold cyan", width=15)
    navigation_table.add_column("Deskripsi", style="white")
    
    navigation_table.add_row("No", "Pilih nomor gambar")
    
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

                image_index = int(choice) - 1

                global_index = start_index + image_index
                
                if 0 <= global_index < len(images):
                    selected_image = images[global_index]
                    return selected_image, page
                else:
                    console.print("[red]Nomor gambar tidak valid.[/red]")
                    cyber_input("Tekan Enter untuk melanjutkan...")
            except ValueError:
                console.print("[red]Input tidak valid. Masukkan nomor gambar, P, N, atau 00.[/red]")
                cyber_input("Tekan Enter untuk melanjutkan...")

def display_image_detail(image_data, page):
    """Menampilkan detail gambar dan pilihan aksi."""
    clear()
    
    detail_content = [
        Text.assemble(("Link Pinterest: ", "bold #00F0FF"), (image_data.get('link', 'N/A'), "link cyan")),
        Text.assemble(("Link Gambar: ", "bold #00F0FF"), (image_data.get('directLink', 'N/A'), "white")),
    ]
    
    detail_panel = Panel(
        Group(*detail_content),
        title="[bold magenta]📌 Detail Gambar 📌[/bold magenta]",
        border_style="medium_purple",
        padding=(1, 2)
    )
    console.print(detail_panel)
    
    console.print("\n[bold cyan]Pilihan untuk gambar ini:[/bold cyan]")
    console.print("[bold cyan]D[/bold cyan][white] Unduh gambar[/white]")
    console.print("[bold cyan]O[/bold cyan][white] Buka di browser[/white]")
    console.print("[bold cyan]0[/bold cyan][white] Kembali ke daftar[/white]")
    
    while True:
        action = cyber_input("Masukkan pilihan: ")
        
        if action == '0':
            return 'back_to_list'
        
        # Aksi: Unduh Gambar
        if action.upper() == 'D':
            image_url_to_download = image_data.get('directLink')
            if not image_url_to_download:
                console.print("[red]Link gambar tidak ditemukan.[/red]")
                cyber_input("Tekan Enter untuk melanjutkan...")
                continue
            
            safe_query = "".join(c for c in image_data.get('name', 'image') if c.isalnum() or c in (' ', '-', '_')).rstrip()
            filename = f"pinterest_{safe_query}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.jpg"
            
            output_path = get_output_path("downloads", filename)
            
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
            }

            try:
                with console.status("[bold green]Mengunduh gambar...[/bold green]", spinner="dots"):
                    image_response = requests.get(image_url_to_download, stream=True, headers=headers)
                    image_response.raise_for_status()
                    
                    with open(output_path, 'wb') as f:
                        for chunk in image_response.iter_content(chunk_size=8192):
                            f.write(chunk)
                
                console.print(f"\n[bold green]✓ Gambar berhasil diunduh![/bold green]")
                console.print(f"[bold cyan]Lokasi:[/bold cyan] {output_path}")
                cyber_input("Tekan Enter untuk kembali ke daftar...")
                return 'back_to_list'
            except requests.exceptions.RequestException as e:
                console.print(f"\n[bold red]Gagal mengunduh gambar: {e}[/bold red]")
                cyber_input("Tekan Enter untuk melanjutkan...")
        
        elif action.upper() == 'O':
            pinterest_url = image_data.get('link')
            if not pinterest_url:
                console.print("[red]Link Pinterest tidak ditemukan.[/red]")
                cyber_input("Tekan Enter untuk melanjutkan...")
                continue
            
            try:
                console.print(f"[bold green]Membuka link Pinterest di browser...[/bold green]")
                webbrowser.open(pinterest_url)
                cyber_input("Tekan Enter untuk kembali ke daftar...")
                return 'back_to_list'
            except Exception as e:
                console.print(f"[red]Gagal membuka browser: {e}[/red]")
                cyber_input("Tekan Enter untuk melanjutkan...")
        
        else:
            console.print("[red]Pilihan tidak valid.[/red]")
            cyber_input("Tekan Enter untuk melanjutkan...")

def pinterest_search():
    """Mencari dan mengunduh gambar di Pinterest."""
    clear()
    print_cyber_panel("Pinterest Search & Download", "Cari dan unduh gambar di platform Pinterest.")
    
    config = load_config()
    if not config or not config.get("base_url"):
        console.print("[bold red]Error: Konfigurasi atau base_url tidak ditemukan.[/bold red]")
        cyber_input("Tekan Enter untuk kembali...")
        return

    search_api_endpoint = f"{config.get('base_url')}/api/search/pinterest"
    
    while True:
        query = cyber_input("Masukkan kata kunci pencarian atau ketik '00' untuk kembali")
        
        if query == '00':
            return

        try:
            with console.status("[bold green]Mencari gambar...[/bold green]", spinner="dots"):
                params = {'query': query}
                response = requests.get(search_api_endpoint, params=params, headers={'accept': 'application/json'})
                response.raise_for_status()
                search_result = response.json()

            if not (search_result and isinstance(search_result, list) and len(search_result) > 0):
                console.print("[bold red]Tidak ada hasil yang ditemukan.[/bold red]")
                cyber_input("Tekan Enter untuk mencari lagi...")
                continue

            current_page = 1
            per_page = 5
            
            while True:
                result_action, new_page = display_pinterest_list(search_result, query, current_page, per_page)
                
                if result_action is None:
                    break
                elif result_action == 'prev_page':
                    current_page = new_page
                elif result_action == 'next_page':
                    current_page = new_page
                else:

                    action_result = display_image_detail(result_action, current_page)
                    
                    if action_result == 'back_to_list':

                        continue

        except requests.exceptions.RequestException as e:
            console.print(f"\n[bold red]Error saat menghubungi API:[/bold red] {e}")
        except Exception as e:
            console.print(f"\n[bold red]Terjadi kesalahan tak terduga:[/bold red] {e}")
        
        cyber_input("\nTekan Enter untuk kembali ke menu Search...")