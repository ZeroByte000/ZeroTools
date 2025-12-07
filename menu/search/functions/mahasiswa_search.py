import requests
import re
from urllib.parse import quote
from core.utils import load_config
from app.console import console, print_cyber_panel, cyber_input, clear
from rich.panel import Panel
from rich.text import Text
from rich.console import Group
from rich.table import Table
from rich.box import SQUARE

def get_mahasiswa_data(config, query):
    """Mengambil data mahasiswa dari API."""
    try:
        api_endpoint = f"{config.get('base_url')}/api/search/mahasiswa"
        with console.status("[bold green]Mencari data mahasiswa...[/bold green]", spinner="dots"):
            params = {'query': query}
            response = requests.get(api_endpoint, params=params, headers={'accept': 'application/json'})
            response.raise_for_status()
            return response.json()
    except requests.exceptions.RequestException as e:
        console.print(f"\n[bold red]Error saat menghubungi API:[/bold red] {e}")
        return None
    except Exception as e:
        console.print(f"\n[bold red]Terjadi kesalahan tak terduga:[/bold red] {e}")
        return None

def is_nim(query):
    return re.match(r'^[A-Za-z]+[0-9]+$', query.strip())

def display_mahasiswa_list(mahasiswa_list, query, page=1, per_page=5):
    """Menampilkan daftar mahasiswa dengan pagination."""
    clear()
    if not mahasiswa_list:
        console.print("[bold red]Tidak ada data mahasiswa yang ditemukan.[/bold red]")
        cyber_input("Tekan Enter untuk kembali...")
        return None, page

    total_pages = (len(mahasiswa_list) + per_page - 1) // per_page
    
    start_index = (page - 1) * per_page
    end_index = min(start_index + per_page, len(mahasiswa_list))
    current_page_data = mahasiswa_list[start_index:end_index]
    
    mahasiswa_panels = []
    
    for i, mahasiswa in enumerate(current_page_data, start=start_index + 1):
        mahasiswa_info = [
            Text.assemble((f"{i}. ", "bold cyan")),
            Text.assemble(("Nama: ", "bold #00F0FF"), (mahasiswa.get('nama', 'N/A'), "white")),
            Text.assemble(("NIM: ", "bold #00F0FF"), (mahasiswa.get('nim', 'N/A'), "white")),
            Text.assemble(("Nama PT: ", "bold #00F0FF"), (mahasiswa.get('nama_pt', 'N/A'), "white")),
            Text.assemble(("Program Studi: ", "bold #00F0FF"), (mahasiswa.get('nama_prodi', 'N/A'), "white")),
        ]
        
        mahasiswa_panel = Panel(
            Group(*mahasiswa_info),
            border_style="medium_purple",
            padding=(0, 1)
        )
        mahasiswa_panels.append(mahasiswa_panel)

    search_type = "NIM" if is_nim(query) else "Nama"

    pagination_info = Text.assemble(
        (f"Halaman {page} dari {total_pages} ", "bold cyan"),
        (f"({len(mahasiswa_list)} total)", "dim")
    )
    
    console.print(Panel(
        Group(*mahasiswa_panels),
        title=f"[bold magenta]🎓 Hasil Pencarian Mahasiswa ({search_type}: '{query}') 🎓[/bold magenta]",
        subtitle=pagination_info,
        border_style="#00F0FF",
        padding=(1, 1)
    ))

    console.print("\n[bold cyan]Navigasi:[/bold cyan]")
    
    navigation_table = Table(show_header=False, box=None, padding=0)
    navigation_table.add_column("Pilihan", style="bold cyan", width=15)
    navigation_table.add_column("Deskripsi", style="white")
    
    navigation_table.add_row("No", "Pilih nomor mahasiswa")
    
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

                mahasiswa_index = int(choice) - 1

                global_index = start_index + mahasiswa_index
                
                if 0 <= global_index < len(mahasiswa_list):
                    selected_mahasiswa = mahasiswa_list[global_index]
                    return selected_mahasiswa, page
                else:
                    console.print("[red]Nomor mahasiswa tidak valid.[/red]")
                    cyber_input("Tekan Enter untuk melanjutkan...")
            except ValueError:
                console.print("[red]Input tidak valid. Masukkan nomor mahasiswa, P, N, atau 00.[/red]")
                cyber_input("Tekan Enter untuk melanjutkan...")

def display_mahasiswa_detail(mahasiswa_data):
    """Menampilkan detail mahasiswa."""
    clear()
    
    info_items = [
        Text.assemble(("Nama: ", "bold #00F0FF"), (mahasiswa_data.get('nama', 'N/A'), "white")),
        Text.assemble(("NIM: ", "bold #00F0FF"), (mahasiswa_data.get('nim', 'N/A'), "white")),
        Text.assemble(("Nama PT: ", "bold #00F0FF"), (mahasiswa_data.get('nama_pt', 'N/A'), "white")),
        Text.assemble(("Program Studi: ", "bold #00F0FF"), (mahasiswa_data.get('nama_prodi', 'N/A'), "white")),
    ]
    
    info_group = Group(*info_items)
    
    panel = Panel(
        info_group,
        title="[bold magenta]🎓 Detail Mahasiswa 🎓[/bold magenta]",
        border_style="medium_purple",
        padding=(1, 2)
    )
    console.print(panel)
    cyber_input("Tekan Enter untuk kembali ke daftar mahasiswa...")

def mahasiswa_search():
    """Mencari data mahasiswa berdasarkan NIM atau nama."""
    clear()
    print_cyber_panel("Search Mahasiswa", "Cari data mahasiswa berdasarkan NIM atau nama.")
    
    config = load_config()
    if not config or not config.get("base_url"):
        console.print("[bold red]Error: Konfigurasi atau base_url tidak ditemukan.[/bold red]")
        cyber_input("Tekan Enter untuk kembali...")
        return

    while True:
        query = cyber_input("Masukkan NIM atau nama mahasiswa atau ketik '00' untuk kembali")
        
        if query == '00':
            return

        try:
            mahasiswa_data = get_mahasiswa_data(config, query)
            
            if not mahasiswa_data:
                cyber_input("Tekan Enter untuk mencoba lagi...")
                continue

            current_page = 1
            per_page = 5  
            if isinstance(mahasiswa_data, dict):
                display_mahasiswa_detail(mahasiswa_data)

            elif is_nim(query):

                filtered_results = [m for m in mahasiswa_data if m.get('nim', '').upper() == query.upper()]
                if filtered_results:
                    if len(filtered_results) == 1:
                        display_mahasiswa_detail(filtered_results[0])
                    else:

                        while True:
                            result, new_page = display_mahasiswa_list(filtered_results, query, current_page, per_page)
                            
                            if result is None:
                                break
                            elif result == 'prev_page':
                                current_page = new_page
                            elif result == 'next_page':
                                current_page = new_page
                            else:

                                display_mahasiswa_detail(result)
                                break
                else:
                    console.print("[bold red]Tidak ada mahasiswa dengan NIM tersebut.[/bold red]")
                    cyber_input("Tekan Enter untuk melanjutkan...")
            else:

                while True:
                    result, new_page = display_mahasiswa_list(mahasiswa_data, query, current_page, per_page)
                    
                    if result is None:
                        break
                    elif result == 'prev_page':
                        current_page = new_page
                    elif result == 'next_page':
                        current_page = new_page
                    else:
                        display_mahasiswa_detail(result)
                        break
            
        except requests.exceptions.RequestException as e:
            console.print(f"\n[bold red]Error saat menghubungi API:[/bold red] {e}")
        except Exception as e:
            console.print(f"\n[bold red]Terjadi kesalahan tak terduga:[/bold red] {e}")
        
        cyber_input("\nTekan Enter untuk kembali ke menu Search...")