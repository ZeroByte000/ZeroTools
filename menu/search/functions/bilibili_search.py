import requests
import webbrowser
from core.utils import load_config
from app.console import console, print_cyber_panel, cyber_input, clear
from rich.panel import Panel
from rich.text import Text
from rich.console import Group
from rich.align import Align
from rich.table import Table
from rich.box import SQUARE

def clean_url(url):
    """Membersihkan URL dari karakter yang tidak diinginkan seperti double slash."""
    if not url:
        return url
    # Mengganti '//' yang muncul setelah domain dengan '/'
    parts = url.split('//')
    if len(parts) > 2:
        # Jika ada lebih dari 2 bagian, gabungkan kembali dengan benar
        # Contoh: ['https:', 'www.bilibili.tv', 'www.bilibili.tv/en/space/1966300736']
        # Menjadi: 'https://www.bilibili.tv/en/space/1966300736'
        return parts[0] + '//' + parts[-1]
    return url

def display_bilibili_list(videos, query, page=1, per_page=5):
    """Menampilkan daftar video Bilibili dengan pagination."""
    clear()
    if not videos:
        console.print("[bold red]Tidak ada video yang ditemukan.[/bold red]")
        cyber_input("Tekan Enter untuk kembali...")
        return None, page

    total_pages = (len(videos) + per_page - 1) // per_page

    start_index = (page - 1) * per_page
    end_index = min(start_index + per_page, len(videos))
    current_page_data = videos[start_index:end_index]
    
    video_panels = []
    
    for i, video in enumerate(current_page_data, start=start_index + 1):
        video_content = [
            Text.assemble((f"{i}. ", "bold cyan")),
            Text.assemble(("Judul: ", "bold #00F0FF"), (video.get('title', 'N/A'), "white")),
            Text.assemble(("Durasi: ", "bold #00F0FF"), (video.get('duration', 'N/A'), "white")),
            Text.assemble(("Views: ", "bold #00F0FF"), (video.get('views', 'N/A'), "white")),
            Text.assemble(("URL: ", "bold #00F0FF"), (video.get('url', 'N/A'), "link cyan")),
        ]
        
        video_panel = Panel(
            Group(*video_content),
            title=f"[bold white]{video.get('uploader', 'N/A')}[/bold white]",
            title_align="left",
            border_style="dim",
            padding=(0, 1)
        )
        video_panels.append(video_panel)

    pagination_info = Text.assemble(
        (f"Halaman {page} dari {total_pages} ", "bold cyan"),
        (f"({len(videos)} total)", "dim")
    )
    
    console.print(Panel(
        Group(*video_panels),
        title=f"[bold magenta]🔍 Hasil Pencarian untuk '{query}'[/bold magenta]",
        subtitle=pagination_info,
        border_style="#00F0FF",
        padding=(1, 1)
    ))
    
    console.print("\n[bold cyan]Navigasi:[/bold cyan]")
    
    navigation_table = Table(show_header=False, box=None, padding=0)
    navigation_table.add_column("Pilihan", style="bold cyan", width=15)
    navigation_table.add_column("Deskripsi", style="white")
    
    navigation_table.add_row("No", "Pilih nomor video untuk membuka di browser")
    
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

                video_index = int(choice) - 1

                global_index = start_index + video_index
                
                if 0 <= global_index < len(videos):
                    selected_video = videos[global_index]

                    video_url = selected_video.get('url', '')
                    if video_url:
                        console.print(f"[bold green]Membuka video di browser...[/bold green]")
                        webbrowser.open(video_url)
                        cyber_input("Tekan Enter untuk melanjutkan...")
                    else:
                        console.print("[red]URL video tidak tersedia.[/red]")
                        cyber_input("Tekan Enter untuk melanjutkan...")
                else:
                    console.print("[red]Nomor video tidak valid.[/red]")
                    cyber_input("Tekan Enter untuk melanjutkan...")
            except ValueError:
                console.print("[red]Input tidak valid. Masukkan nomor video, P, N, atau 00.[/red]")
                cyber_input("Tekan Enter untuk melanjutkan...")

def bilibili_search():
    """Mencari video di Bilibili."""
    clear()
    print_cyber_panel("Bilibili Search", "Cari video di platform Bilibili.")
    
    config = load_config()
    if not config or not config.get("base_url"):
        console.print("[bold red]Error: Konfigurasi atau base_url tidak ditemukan.[/bold red]")
        cyber_input("Tekan Enter untuk kembali...")
        return

    api_endpoint = f"{config.get('base_url')}/api/search/bilibili"
    
    while True:
        query = cyber_input("Masukkan kata kunci pencarian atau ketik '00' untuk kembali")
        
        if query == '00':
            return

        try:
            with console.status("[bold green]Mencari video...[/bold green]", spinner="dots"):
                params = {'query': query}
                response = requests.get(api_endpoint, params=params, headers={'accept': 'application/json'})
                response.raise_for_status()
                result = response.json()

            if result and isinstance(result, list) and len(result) > 0:

                for video in result:
                    if 'url' in video:
                        video['url'] = clean_url(video['url'])

                current_page = 1
                per_page = 5  
                
                while True:
                    result_action, new_page = display_bilibili_list(result, query, current_page, per_page)
                    
                    if result_action is None:
                        break  
                    elif result_action == 'prev_page':
                        current_page = new_page
                    elif result_action == 'next_page':
                        current_page = new_page

            else:
                console.print("[bold red]Tidak ada hasil yang ditemukan atau terjadi kesalahan.[/bold red]")

        except requests.exceptions.RequestException as e:
            console.print(f"\n[bold red]Error saat menghubungi API:[/bold red] {e}")
        except Exception as e:
            console.print(f"\n[bold red]Terjadi kesalahan tak terduga:[/bold red] {e}")
        
        cyber_input("\nTekan Enter untuk kembali ke menu Search...")