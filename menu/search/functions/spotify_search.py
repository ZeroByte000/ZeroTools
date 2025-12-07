import requests
import os
import json
from datetime import datetime
from urllib.parse import quote
from core.utils import load_config, get_output_path
from app.console import console, print_cyber_panel, cyber_input, clear
from rich.panel import Panel
from rich.text import Text
from rich.console import Group
from rich.align import Align
from rich.table import Table
from rich.box import SQUARE

def display_spotify_info(data):
    clear()
    info_items = []
    
    title = data.get("name", "Unknown Title")
    artists = data.get("artists", [])
    album = data.get("album", {})
    url = data.get("url", "")
    popularity = data.get("popularity", 0)
    duration_ms = data.get("duration_ms", 0)
    
    info_items.append(Text.assemble(("Judul: ", "bold #00F0FF"), (title, "white")))
    
    if artists:
        artist_names = ", ".join(artists)
        info_items.append(Text.assemble(("Artis: ", "bold #00F0FF"), (artist_names, "white")))
    
    if album:
        album_name = album.get("name", "Unknown Album")
        album_release_date = album.get("release_date", "Unknown Date")
        info_items.append(Text.assemble(("Album: ", "bold #00F0FF"), (f"{album_name} ({album_release_date})", "white")))
    
    if popularity > 0:
        info_items.append(Text.assemble(("Popularitas: ", "bold #00F0FF"), (f"{popularity:,}", "white")))
    if duration_ms > 0:
        duration_str = f"{duration_ms // 60000}:{(duration_ms % 60000):02d}"
        info_items.append(Text.assemble(("Durasi: ", "bold #00F0FF"), (duration_str, "white")))
    
    if url:
        info_items.append(Text.assemble(("URL: ", "bold #00F0FF"), (url, "link cyan")))
    
    info_group = Group(*info_items)
    
    panel = Panel(
        info_group,
        title="[bold magenta]🎵 Informasi Lagu Spotify 🎵[/bold magenta]",
        border_style="medium_purple",
        padding=(1, 2)
    )
    console.print(panel)

def display_artist_info(data):
    clear()
    info_items = []
    
    name = data.get("name", "Unknown Artist")
    followers = data.get("followers", 0)
    genres = data.get("genres", [])
    popularity = data.get("popularity", 0)
    url = data.get("url", "")
    image_url = data.get("image", "")
    
    info_items.append(Text.assemble(("Nama Artis: ", "bold #00F0FF"), (name, "white")))
    
    if followers > 0:
        info_items.append(Text.assemble(("Pengikut: ", "bold #00F0FF"), (f"{followers:,}", "white")))
    if popularity > 0:
        info_items.append(Text.assemble(("Popularitas: ", "bold #00F0FF"), (f"{popularity:,}", "white")))
    if genres:
        genre_str = ', '.join(genres)
        info_items.append(Text.assemble(("Genre: ", "bold #00F0FF"), (genre_str, "white")))
    
    if url:
        info_items.append(Text.assemble(("URL: ", "bold #00F0FF"), (url, "link cyan")))
    
    if image_url:
        info_items.append(Text.assemble(("Gambar: ", "bold #00F0FF"), (image_url, "link cyan")))
    
    info_group = Group(*info_items)
    
    panel = Panel(
        info_group,
        title="[bold magenta]👤 Informasi Artis Spotify 👤[/bold magenta]",
        border_style="medium_purple",
        padding=(1, 2)
    )
    console.print(panel)

def display_album_info(data):
    clear()
    info_items = []
    
    name = data.get("name", "Unknown Album")
    artists = data.get("artists", [])
    release_date = data.get("release_date", "Unknown Date")
    total_tracks = data.get("total_tracks", 0)
    url = data.get("url", "")
    image_url = data.get("image", "")
    
    info_items.append(Text.assemble(("Judul Album: ", "bold #00F0FF"), (name, "white")))
    
    if artists:
        artist_names = ", ".join(artists)
        info_items.append(Text.assemble(("Artis: ", "bold #00F0FF"), (artist_names, "white")))
    
    if release_date != "Unknown Date":
        info_items.append(Text.assemble(("Tanggal Rilis: ", "bold #00F0FF"), (release_date, "white")))
    if total_tracks > 0:
        info_items.append(Text.assemble(("Total Lagu: ", "bold #00F0FF"), (f"{total_tracks} lagu", "white")))
    
    if url:
        info_items.append(Text.assemble(("URL: ", "bold #00F0FF"), (url, "link cyan")))
    
    if image_url:
        info_items.append(Text.assemble(("Cover: ", "bold #00F0FF"), (image_url, "link cyan")))
    
    info_group = Group(*info_items)
    
    panel = Panel(
        info_group,
        title="[bold magenta]🎶 Informasi Album Spotify 🎶[/bold magenta]",
        border_style="medium_purple",
        padding=(1, 2)
    )
    console.print(panel)

def display_playlist_info(data):
    clear()
    info_items = []
    
    name = data.get("name", "Unknown Playlist")
    owner = data.get("owner", "Unknown Owner")
    total_tracks = data.get("tracks_total", 0)
    description = data.get("description", "Tidak ada deskripsi.")
    url = data.get("url", "")
    image_url = data.get("image", "")
    
    info_items.append(Text.assemble(("Judul Playlist: ", "bold #00F0FF"), (name, "white")))
    info_items.append(Text.assemble(("Pemilik: ", "bold #00F0FF"), (owner, "white")))
    
    if total_tracks > 0:
        info_items.append(Text.assemble(("Total Lagu: ", "bold #00F0FF"), (f"{total_tracks} lagu", "white")))
    if description and description != "Tidak ada deskripsi.":
        info_items.append(Text.assemble(("Deskripsi: ", "bold #00F0FF"), (description, "white")))
    
    if url:
        info_items.append(Text.assemble(("URL: ", "bold #00F0FF"), (url, "link cyan")))
    
    if image_url:
        info_items.append(Text.assemble(("Cover: ", "bold #00F0FF"), (image_url, "link cyan")))
    
    info_group = Group(*info_items)
    
    panel = Panel(
        info_group,
        title="[bold magenta]🎶 Informasi Playlist Spotify 🎶[/bold magenta]",
        border_style="medium_purple",
        padding=(1, 2)
    )
    console.print(panel)

def download_spotify_track(track_url, track_name, artists):
    try:
        with console.status("[bold green]Mengambil informasi lagu...[/bold green]", spinner="dots"):
            config = load_config()
            if not config or not config.get("base_url"):
                console.print("[bold red]Error: Konfigurasi atau base_url tidak ditemukan.[/bold red]")
                return False

            base_url = config.get("base_url")
            api_endpoint = f"{base_url}/api/downloader/spotify"
            
            encoded_url = quote(track_url)
            
            response = requests.get(f"{api_endpoint}?url={encoded_url}")
            response.raise_for_status()
            result = response.json()

        if result.get("success"):
            display_downloaded_track_info(result)
            
            download_url = result.get("link", "")
            
            if not download_url:
                console.print("[bold red]URL unduhan tidak tersedia.[/bold red]")
                return False

            safe_title = "".join(c for c in f"{track_name} - {', '.join(artists)}" if c.isalnum() or c in (' ', '-', '_')).rstrip()
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
            log_filename = f"spotify_download_log_{timestamp}.json"
            log_path = get_output_path("output", log_filename, no_prompt=True)
            
            with open(log_path, 'w') as f:
                json.dump(result, f, indent=4)
            
            console.print(f"[dim]Log respons disimpan di: {log_path}[/dim]")
            return True
        else:
            console.print(f"[bold red]Gagal mengambil informasi lagu.[/bold red]")
            console.print(f"Detail dari server: {result}")
            return False

    except requests.exceptions.RequestException as e:
        console.print(f"\n[bold red]Error saat menghubungi API:[/bold red] {e}")
        return False
    except Exception as e:
        console.print(f"\n[bold red]Terjadi kesalahan tak terduga:[/bold red] {e}")
        return False

def display_downloaded_track_info(data):
    clear()
    metadata = data.get("metadata", {})
    
    info_items = []
    
    title = metadata.get("title", "Unknown Title")
    artists = metadata.get("artists", "Unknown Artist")
    album = metadata.get("album", "Unknown Album")
    release_date = metadata.get("releaseDate", "Unknown")
    cover = metadata.get("cover", "")
    
    info_items.append(Text.assemble(("Judul: ", "bold cyan"), (title, "white")))
    info_items.append(Text.assemble(("Artis: ", "bold cyan"), (artists, "white")))
    info_items.append(Text.assemble(("Album: ", "bold cyan"), (album, "white")))
    info_items.append(Text.assemble(("Rilis: ", "bold cyan"), (release_date, "white")))
    
    if cover:
        info_items.append(Text.assemble(("Cover: ", "bold cyan"), (cover, "white")))

    info_group = Group(*info_items)
    
    panel = Panel(
        info_group,
        title="[bold magenta]🎵 Informasi Lagu 🎵[/bold magenta]",
        border_style="medium_purple",
        padding=(1, 2)
    )
    console.print(panel)

def display_tracks_with_options(tracks, page=1, per_page=5):
    """Menampilkan daftar lagu dengan pagination."""
    clear()
    console.print("[bold green]Daftar Lagu Spotify:[/bold green]")
    
    # Hitung total halaman
    total_pages = (len(tracks) + per_page - 1) // per_page
    
    # Ambil data untuk halaman saat ini
    start_index = (page - 1) * per_page
    end_index = min(start_index + per_page, len(tracks))
    current_page_data = tracks[start_index:end_index]
    
    track_panels = []
    
    for i, track in enumerate(current_page_data, start=start_index + 1):
        title = track.get("name", "Unknown Title")
        artists = track.get("artists", [])
        album = track.get("album", {}).get("name", "Unknown Album")
        duration = track.get("duration_ms", 0)
        
        track_info = Text.assemble(
            (f"{i}. ", "bold cyan"),
            (title, "bold white"),
            ("\n   Artis: ", "cyan"),
            (", ".join(artists) if artists else "Unknown Artist", "white"),
            ("\n   Album: ", "cyan"),
            (album, "white"),
            ("\n   Durasi: ", "cyan"),
            (f"{duration // 60000}:{(duration % 60000):02d}" if duration > 0 else "Unknown", "white")
        )
        
        track_panel = Panel(
            track_info,
            border_style="medium_purple",
            padding=(0, 1)
        )
        track_panels.append(track_panel)
    
    # Tampilkan informasi pagination
    pagination_info = Text.assemble(
        (f"Halaman {page} dari {total_pages} ", "bold cyan"),
        (f"({len(tracks)} total)", "dim")
    )
    
    console.print(Panel(
        Group(*track_panels),
        title=f"[bold magenta]🎵 Hasil Pencarian Spotify 🎵[/bold magenta]",
        subtitle=pagination_info,
        border_style="#00F0FF",
        padding=(1, 1)
    ))
    
    # Tampilkan navigasi pagination
    console.print("\n[bold cyan]Navigasi:[/bold cyan]")
    
    navigation_table = Table(show_header=False, box=None, padding=0)
    navigation_table.add_column("Pilihan", style="bold cyan", width=15)
    navigation_table.add_column("Deskripsi", style="white")
    
    navigation_table.add_row("No", "Pilih nomor lagu untuk melihat detail")
    
    if page > 1:
        navigation_table.add_row("P", f"Halaman sebelumnya ({page-1})")
    
    if page < total_pages:
        navigation_table.add_row("N", f"Halaman berikutnya ({page+1})")
    
    navigation_table.add_row("D", "Unduh lagu")
    navigation_table.add_row("00", "Kembali ke pencarian")
    
    console.print(navigation_table)
    
    while True:
        choice = cyber_input("Masukkan pilihan: ")
        
        if choice == '00':
            return None, page
        
        # Navigasi pagination
        elif choice.upper() == 'P' and page > 1:
            return 'prev_page', page - 1
        elif choice.upper() == 'N' and page < total_pages:
            return 'next_page', page + 1
        
        # Unduh lagu
        elif choice.upper() == 'D':
            track_choice = cyber_input("Pilih nomor lagu untuk diunduh: ")
            try:
                track_index = int(track_choice) - 1
                # Konversi ke index global
                global_index = start_index + track_index
                
                if 0 <= global_index < len(tracks):
                    selected_track = tracks[global_index]
                    track_url = selected_track.get("url", "")
                    track_name = selected_track.get("name", "Unknown Title")
                    artists = selected_track.get("artists", ["Unknown Artist"])
                    
                    if track_url:
                        if download_spotify_track(track_url, track_name, artists):
                            cyber_input("Tekan Enter untuk melanjutkan...")
                            return 'downloaded', page
                    else:
                        console.print("[red]URL lagu tidak tersedia.[/red]")
                        cyber_input("Tekan Enter untuk melanjutkan...")
                else:
                    console.print("[red]Nomor lagu tidak valid.[/red]")
                    cyber_input("Tekan Enter untuk melanjutkan...")
            except ValueError:
                console.print("[red]Input tidak valid. Masukkan nomor lagu.[/red]")
                cyber_input("Tekan Enter untuk melanjutkan...")
        
        # Pilih lagu
        else:
            try:
                track_index = int(choice) - 1
                # Konversi ke index global
                global_index = start_index + track_index
                
                if 0 <= global_index < len(tracks):
                    selected_track = tracks[global_index]
                    display_spotify_info(selected_track)
                    
                    console.print("\n[bold cyan]Pilihan untuk lagu ini:[/bold cyan]")
                    console.print("[bold cyan]D[/bold cyan][white]Unduh lagu[/white]")
                    console.print("[bold cyan]00[/bold cyan][white]Kembali ke daftar[/white]")
                    
                    action = cyber_input("Masukkan pilihan: ")
                    
                    if action == '00':
                        return 'back_to_list'
                    elif action.upper() == 'D':
                        track_url = selected_track.get("url", "")
                        track_name = selected_track.get("name", "Unknown Title")
                        artists = selected_track.get("artists", ["Unknown Artist"])
                        
                        if track_url:
                            if download_spotify_track(track_url, track_name, artists):
                                cyber_input("Tekan Enter untuk melanjutkan...")
                                return 'downloaded', page
                            else:
                                console.print("[red]URL lagu tidak tersedia.[/red]")
                                cyber_input("Tekan Enter untuk melanjutkan...")
                    else:
                        console.print("[red]Pilihan tidak valid.[/red]")
                        cyber_input("Tekan Enter untuk melanjutkan...")
            except ValueError:
                console.print("[red]Input tidak valid. Masukkan nomor lagu, P, N, D, atau 00.[/red]")
                cyber_input("Tekan Enter untuk melanjutkan...")
    

def display_albums_with_options(albums, page=1, per_page=5):
    """Menampilkan daftar album dengan pagination."""
    clear()
    console.print("[bold green]Daftar Album Spotify:[/bold green]")
    
    total_pages = (len(albums) + per_page - 1) // per_page
    
    start_index = (page - 1) * per_page
    end_index = min(start_index + per_page, len(albums))
    current_page_data = albums[start_index:end_index]
    
    album_panels = []
    
    for i, album in enumerate(current_page_data, start=start_index + 1):
        name = album.get("name", "Unknown Album")
        artists = album.get("artists", [])
        release_date = album.get("release_date", "Unknown Date")
        total_tracks = album.get("total_tracks", 0)
        
        album_info = Text.assemble(
            (f"{i}. ", "bold cyan"),
            (name, "bold white"),
            ("\n   Artis: ", "cyan"),
            (", ".join(artists) if artists else "Unknown Artist", "white"),
            ("\n   Rilis: ", "cyan"),
            (release_date, "white"),
            ("\n   Total Lagu: ", "cyan"),
            (f"{total_tracks}", "white")
        )
        
        album_panel = Panel(
            album_info,
            border_style="medium_purple",
            padding=(0, 1)
        )
        album_panels.append(album_panel)
    
    pagination_info = Text.assemble(
        (f"Halaman {page} dari {total_pages} ", "bold cyan"),
        (f"({len(albums)} total)", "dim")
    )
    
    console.print(Panel(
        Group(*album_panels),
        title=f"[bold magenta]🎶 Hasil Pencarian Spotify 🎶[/bold magenta]",
        subtitle=pagination_info,
        border_style="#00F0FF",
        padding=(1, 1)
    ))
    
    console.print("\n[bold cyan]Navigasi:[/bold cyan]")
    
    navigation_table = Table(show_header=False, box=None, padding=0)
    navigation_table.add_column("Pilihan", style="bold cyan", width=15)
    navigation_table.add_column("Deskripsi", style="white")
    
    navigation_table.add_row("1-5", "Pilih nomor album untuk melihat detail")
    
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
                album_index = int(choice) - 1
                global_index = start_index + album_index
                
                if 0 <= global_index < len(albums):
                    selected_album = albums[global_index]
                    display_album_info(selected_album)
                    
                    console.print("\n[bold cyan]Pilihan untuk album ini:[/bold cyan]")
                    console.print("[bold cyan]00[/bold cyan][white]Kembali ke daftar[/white]")
                    
                    action = cyber_input("Masukkan pilihan: ")
                    
                    if action == '00':
                        return 'back_to_list'
                    else:
                        console.print("[red]Pilihan tidak valid.[/red]")
                        cyber_input("Tekan Enter untuk melanjutkan...")
            except ValueError:
                console.print("[red]Input tidak valid. Masukkan nomor album, P, N, atau 00.[/red]")
                cyber_input("Tekan Enter untuk melanjutkan...")
    
def display_artists_with_options(artists, page=1, per_page=5):
    """Menampilkan daftar artis dengan pagination."""
    clear()
    console.print("[bold green]Daftar Artis Spotify:[/bold green]")

    total_pages = (len(artists) + per_page - 1) // per_page

    start_index = (page - 1) * per_page
    end_index = min(start_index + per_page, len(artists))
    current_page_data = artists[start_index:end_index]
    
    artist_panels = []
    
    for i, artist in enumerate(current_page_data, start=start_index + 1):
        name = artist.get("name", "Unknown Artist")
        followers = artist.get("followers", 0)
        genres = artist.get("genres", [])
        popularity = artist.get("popularity", 0)
        
        artist_info = Text.assemble(
            (f"{i}. ", "bold cyan"),
            (name, "bold white"),
            ("\n   Pengikut: ", "cyan"),
            (f"{followers:,}" if followers > 0 else "N/A", "white"),
            ("\n   Genre: ", "cyan"),
            (", ".join(genres) if genres else "N/A", "white"),
            ("\n   Popularitas: ", "cyan"),
            (f"{popularity:,}" if popularity > 0 else "N/A", "white")
        )
        
        artist_panel = Panel(
            artist_info,
            border_style="medium_purple",
            padding=(0, 1)
        )
        artist_panels.append(artist_panel)
    
    pagination_info = Text.assemble(
        (f"Halaman {page} dari {total_pages} ", "bold cyan"),
        (f"({len(artists)} total)", "dim")
    )
    
    console.print(Panel(
        Group(*artist_panels),
        title=f"[bold magenta]👤 Hasil Pencarian Spotify 🎵[/bold magenta]",
        subtitle=pagination_info,
        border_style="#00F0FF",
        padding=(1, 1)
    ))
    
    console.print("\n[bold cyan]Navigasi:[/bold cyan]")
    
    navigation_table = Table(show_header=False, box=None, padding=0)
    navigation_table.add_column("Pilihan", style="bold cyan", width=15)
    navigation_table.add_column("Deskripsi", style="white")
    
    navigation_table.add_row("1-5", "Pilih nomor artis untuk melihat detail")
    
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
                artist_index = int(choice) - 1
                # Konversi ke index global
                global_index = start_index + artist_index
                
                if 0 <= global_index < len(artists):
                    selected_artist = artists[global_index]
                    display_artist_info(selected_artist)
                    
                    console.print("\n[bold cyan]Pilihan untuk artis ini:[/bold cyan]")
                    console.print("[bold cyan]00[/bold cyan][white]Kembali ke daftar[/white]")
                    
                    action = cyber_input("Masukkan pilihan: ")
                    
                    if action == '00':
                        return 'back_to_list'
                    else:
                        console.print("[red]Pilihan tidak valid.[/red]")
                        cyber_input("Tekan Enter untuk melanjutkan...")
            except ValueError:
                console.print("[red]Input tidak valid. Masukkan nomor artis, P, N, atau 00.[/red]")
                cyber_input("Tekan Enter untuk melanjutkan...")
    
def display_playlists_with_options(playlists, page=1, per_page=5):
    """Menampilkan daftar playlist dengan pagination."""
    clear()
    console.print("[bold green]Daftar Playlist Spotify:[/bold green]")

    total_pages = (len(playlists) + per_page - 1) // per_page

    start_index = (page - 1) * per_page
    end_index = min(start_index + per_page, len(playlists))
    current_page_data = playlists[start_index:end_index]
    
    playlist_panels = []
    
    for i, playlist in enumerate(current_page_data, start=start_index + 1):
        name = playlist.get("name", "Unknown Playlist")
        owner = playlist.get("owner", "Unknown Owner")
        total_tracks = playlist.get("tracks_total", 0)
        description = playlist.get("description", "Tidak ada deskripsi.")
        
        playlist_info = Text.assemble(
            (f"{i}. ", "bold cyan"),
            (name, "bold white"),
            ("\n   Pemilik: ", "cyan"),
            (owner, "white"),
            ("\n   Total Lagu: ", "cyan"),
            (f"{total_tracks}" if total_tracks > 0 else "N/A", "white")
        )
        
        if description and description != "Tidak ada deskripsi.":
            playlist_info.append(("\n   Deskripsi: ", "cyan"))
            desc_text = description[:100] + "..." if len(description) > 100 else description
            playlist_info.append((desc_text, "white"))
        
        playlist_panel = Panel(
            playlist_info,
            border_style="medium_purple",
            padding=(0, 1)
        )
        playlist_panels.append(playlist_panel)

    pagination_info = Text.assemble(
        (f"Halaman {page} dari {total_pages} ", "bold cyan"),
        (f"({len(playlists)} total)", "dim")
    )
    
    console.print(Panel(
        Group(*playlist_panels),
        title=f"[bold magenta]🎶 Hasil Pencarian Spotify 🎵[/bold magenta]",
        subtitle=pagination_info,
        border_style="#00F0FF",
        padding=(1, 1)
    ))
    
    console.print("\n[bold cyan]Navigasi:[/bold cyan]")
    
    navigation_table = Table(show_header=False, box=None, padding=0)
    navigation_table.add_column("Pilihan", style="bold cyan", width=15)
    navigation_table.add_column("Deskripsi", style="white")
    
    navigation_table.add_row("1-5", "Pilih nomor playlist untuk melihat detail")
    
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
                playlist_index = int(choice) - 1
                # Konversi ke index global
                global_index = start_index + playlist_index
                
                if 0 <= global_index < len(playlists):
                    selected_playlist = playlists[global_index]
                    display_playlist_info(selected_playlist)
                    
                    console.print("\n[bold cyan]Pilihan untuk playlist ini:[/bold cyan]")
                    console.print("[bold cyan]00[/bold cyan][white]Kembali ke daftar[/white]")
                    
                    action = cyber_input("Masukkan pilihan: ")
                    
                    if action == '00':
                        return 'back_to_list'
                    else:
                        console.print("[red]Pilihan tidak valid.[/red]")
                        cyber_input("Tekan Enter untuk melanjutkan...")
            except ValueError:
                console.print("[red]Input tidak valid. Masukkan nomor playlist, P, N, atau 00.[/red]")
                cyber_input("Tekan Enter untuk melanjutkan...")

def spotify_search():
    """Mencari lagu, artis, album, atau playlist di Spotify."""
    clear()
    print_cyber_panel("Spotify Search", "Cari lagu, artis, album, atau playlist di Spotify.")
    
    config = load_config()
    if not config or not config.get("base_url"):
        console.print("[bold red]Error: Konfigurasi atau base_url tidak ditemukan.[/bold red]")
        cyber_input("Tekan Enter untuk kembali...")
        return

    search_api_endpoint = f"{config.get('base_url')}/api/search/spotify"
    
    while True:
        query = cyber_input("Masukkan kata kunci pencarian atau ketik '00' untuk kembali")
        
        if query == '00':
            return

        try:
            with console.status("[bold green]Mencari di Spotify...[/bold green]", spinner="dots"):
                params = {'query': query}
                response = requests.get(search_api_endpoint, params=params, headers={'accept': 'application/json'})
                response.raise_for_status()
                search_result = response.json()

            if search_result:
                tracks = search_result.get("tracks", [])
                albums = search_result.get("albums", [])
                artists = search_result.get("artists", [])
                playlists = search_result.get("playlists", [])
                
                if tracks:
                    current_page = 1
                    per_page = 5 
                    
                    while True:
                        result_action, new_page = display_tracks_with_options(tracks, current_page, per_page)
                        
                        if result_action is None:
                            break 
                        elif result_action == 'prev_page':
                            current_page = new_page
                        elif result_action == 'next_page':
                            current_page = new_page
                        elif result_action == 'downloaded':
                            continue
                        elif result_action == 'back_to_list':

                            result_action, new_page = display_tracks_with_options(tracks, current_page, per_page)
                            
                            if result_action is None:
                                break  
                            elif result_action == 'prev_page':
                                current_page = new_page
                            elif result_action == 'next_page':
                                current_page = new_page
                            elif result_action == 'downloaded':
                                continue
                        else:
                            continue
                
                elif artists:
                    current_page = 1
                    per_page = 5  
                    
                    while True:
                        result_action, new_page = display_artists_with_options(artists, current_page, per_page)
                        
                        if result_action is None:
                            break  
                        elif result_action == 'prev_page':
                            current_page = new_page
                        elif result_action == 'next_page':
                            current_page = new_page
                        else:
                            continue
                
                elif albums:

                    current_page = 1
                    per_page = 5  
                    
                    while True:
                        result_action, new_page = display_albums_with_options(albums, current_page, per_page)
                        
                        if result_action is None:
                            break  
                        elif result_action == 'prev_page':
                            current_page = new_page
                        elif result_action == 'next_page':
                            current_page = new_page
                        else:
                            continue
                
                elif playlists:
                    current_page = 1
                    per_page = 5  
                    
                    while True:
                        result_action, new_page = display_playlists_with_options(playlists, current_page, per_page)
                        
                        if result_action is None:
                            break  
                        elif result_action == 'prev_page':
                            current_page = new_page
                        elif result_action == 'next_page':
                            current_page = new_page
                        else:
                            continue
                else:
                    console.print("[bold red]Tidak ada hasil yang ditemukan.[/bold red]")
            
        except requests.exceptions.RequestException as e:
            console.print(f"\n[bold red]Error saat menghubungi API:[/bold red] {e}")
        except Exception as e:
            console.print(f"\n[bold red]Terjadi kesalahan tak terduga:[/bold red] {e}")
        
        cyber_input("\nTekan Enter untuk kembali ke menu Search...")