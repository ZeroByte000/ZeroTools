import requests
import json
from urllib.parse import quote

# Import fungsi konfigurasi dan console
from core.utils import load_config
from app.console import console, print_cyber_panel, cyber_input, clear

# Import komponen Rich
from rich.panel import Panel
from rich.text import Text
from rich.console import Group
from rich.table import Table
from rich.box import SQUARE

def get_lyrics_data(config, query):
    """Mengambil data lirik dari API."""
    try:
        api_endpoint = f"{config.get('base_url')}/api/search/lyrics"
        with console.status("[bold green]Mencari lirik...[/bold green]", spinner="dots"):
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

def display_lyrics_list(lyrics_list, query):
    """Menampilkan daftar lirik yang ditemukan."""
    clear()
    if not lyrics_list:
        console.print("[bold red]Tidak ada lirik yang ditemukan.[/bold red]")
        cyber_input("Tekan Enter untuk kembali...")
        return None

    lyrics_panels = []
    
    for i, lyric in enumerate(lyrics_list):
        lyric_info = [
            Text.assemble((f"{i+1}. ", "bold cyan")),
            Text.assemble(("Judul: ", "bold #00F0FF"), (lyric.get('name', 'N/A'), "white")),
            Text.assemble(("Artis: ", "bold #00F0FF"), (lyric.get('artistName', 'N/A'), "white")),
            Text.assemble(("Album: ", "bold #00F0FF"), (lyric.get('albumName', 'N/A'), "white")),
            Text.assemble(("Durasi: ", "bold #00F0FF"), (f"{lyric.get('duration', 0)} detik", "white")),
        ]
        
        lyric_panel = Panel(
            Group(*lyric_info),
            border_style="medium_purple",
            padding=(0, 1)
        )
        lyrics_panels.append(lyric_panel)

    console.print(Panel(
        Group(*lyrics_panels),
        title=f"[bold magenta]🎵 Hasil Pencarian Lirik untuk '{query}' 🎵[/bold magenta]",
        border_style="#00F0FF",
        padding=(1, 1)
    ))
    
    console.print("\n[bold cyan]Pilihan:[/bold cyan]")
    console.print("[bold cyan]1-[/bold cyan][white] Pilih nomor lirik untuk melihat detail[/white]")
    console.print("[bold cyan]00[/bold cyan][white] Kembali ke pencarian[/white]")
    
    while True:
        choice = cyber_input("Masukkan pilihan: ")
        
        if choice == '00':
            return None
        
        try:
            lyric_index = int(choice) - 1
            if 0 <= lyric_index < len(lyrics_list):
                selected_lyric = lyrics_list[lyric_index]
                return selected_lyric
            else:
                console.print("[red]Nomor lirik tidak valid. Kembali ke daftar lirik.[/red]")
                cyber_input("Tekan Enter untuk melanjutkan...")
                return None # Langsung kembali ke daftar
        except ValueError:
            console.print("[red]Input tidak valid. Kembali ke daftar lirik.[/red]")
            cyber_input("Tekan Enter untuk melanjutkan...")
            return None # Langsung kembali ke daftar

def display_synced_lyrics(synced_lyrics):
    """Menampilkan lirik sinkronisasi."""
    clear()
    if not synced_lyrics:
        console.print("[bold red]Lirik sinkronisasi tidak tersedia.[/bold red]")
        cyber_input("Tekan Enter untuk kembali ke daftar lirik...")
        return 'back_to_list'
    
    lyrics_text = Text(synced_lyrics, style="white")
    lyrics_panel = Panel(
        lyrics_text,
        title="[bold magenta]⏱️ Lirik Sinkronisasi ⏱️[/bold magenta]",
        border_style="medium_purple",
        padding=(1, 2)
    )
    console.print(lyrics_panel)
    cyber_input("Tekan Enter untuk kembali ke detail lirik...")
    return 'back_to_detail'

def display_lyrics_detail(lyric_data):
    """Menampilkan detail lirik lengkap."""
    clear()
    
    info_items = [
        Text.assemble(("Judul: ", "bold #00F0FF"), (lyric_data.get('name', 'N/A'), "white")),
        Text.assemble(("Artis: ", "bold #00F0FF"), (lyric_data.get('artistName', 'N/A'), "white")),
        Text.assemble(("Album: ", "bold #00F0FF"), (lyric_data.get('albumName', 'N/A'), "white")),
        Text.assemble(("Durasi: ", "bold #00F0FF"), (f"{lyric_data.get('duration', 0)} detik", "white")),
        Text.assemble(("Instrumental: ", "bold #00F0FF"), ("Ya" if lyric_data.get('instrumental', False) else "Tidak", "white")),
    ]
    
    info_group = Group(*info_items)
    
    info_panel = Panel(
        info_group,
        title="[bold magenta]🎵 Informasi Lagu 🎵[/bold magenta]",
        border_style="medium_purple",
        padding=(1, 2)
    )
    console.print(info_panel)
    
    # Tampilkan lirik
    plain_lyrics = lyric_data.get('plainLyrics', '')
    if plain_lyrics:
        lyrics_text = Text(plain_lyrics, style="white")
        lyrics_panel = Panel(
            lyrics_text,
            title="[bold magenta]📝 Lirik Lagu 📝[/bold magenta]",
            border_style="medium_purple",
            padding=(1, 2)
        )
        console.print(lyrics_panel)
    
    console.print("\n[bold cyan]Pilihan:[/bold cyan]")
    console.print("[bold cyan]S[/bold cyan][white] Tampilkan lirik sinkronisasi[/white]")
    console.print("[bold cyan]00[/bold cyan][white] Kembali ke daftar lirik[/white]")
    
    while True:
        choice = cyber_input("Masukkan pilihan: ")
        
        if choice == '00':
            return 'back_to_list'
        elif choice.upper() == 'S':
            result = display_synced_lyrics(lyric_data.get('syncedLyrics', None))
            if result == 'back_to_list':
                return 'back_to_list'
            # Jika kembali ke detail, lanjutkan loop
        else:
            console.print("[red]Pilihan tidak valid. Kembali ke daftar lirik.[/red]")
            cyber_input("Tekan Enter untuk melanjutkan...")
            return 'back_to_list' # Langsung kembali ke daftar

def music_lyrics_search():
    """Mencari lirik lagu."""
    clear()
    print_cyber_panel("Music Lyrics Search", "Cari lirik lagu dari berbagai artis.")
    
    config = load_config()
    if not config or not config.get("base_url"):
        console.print("[bold red]Error: Konfigurasi atau base_url tidak ditemukan.[/bold red]")
        cyber_input("Tekan Enter untuk kembali...")
        return

    while True:
        query = cyber_input("Masukkan judul lagu atau nama artis atau ketik '00' untuk kembali")
        
        if query == '00':
            return

        try:
            lyrics_data = get_lyrics_data(config, query)
            
            if not lyrics_data:
                cyber_input("Tekan Enter untuk mencoba lagi...")
                continue
            
            # Tampilkan daftar lirik
            selected_lyric = display_lyrics_list(lyrics_data, query)
            
            if selected_lyric:
                # Tampilkan detail lirik
                result = display_lyrics_detail(selected_lyric)
                
                if result == 'back_to_list':
                    # Kembali ke daftar lirik
                    selected_lyric = display_lyrics_list(lyrics_data, query)
                    if selected_lyric:
                        display_lyrics_detail(selected_lyric)
            
        except requests.exceptions.RequestException as e:
            console.print(f"\n[bold red]Error saat menghubungi API:[/bold red] {e}")
        except Exception as e:
            console.print(f"\n[bold red]Terjadi kesalahan tak terduga:[/bold red] {e}")
        
        cyber_input("\nTekan Enter untuk kembali ke menu Search...")