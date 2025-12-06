# core/utils.py

import requests
import os
import json
import time
import re

from bs4 import BeautifulSoup
from app.console import console, cyber_input

def load_config():
    """Memuat konfigurasi dari file core/config.json."""
    try:
        base_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        config_path = os.path.join(base_path, 'core', 'config.json')
        
        with open(config_path, 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        console.print("[bold red]Error: 'core/config.json' not found.[/bold red]")
        return None
    except json.JSONDecodeError:
        console.print("[bold red]Error: 'core/config.json' is not a valid JSON file.[/bold red]")
        return None

def upload_to_imgbb_no_api(image_path: str) -> str | None:
    """Mengunggah gambar ke ImgBB tanpa API key, dengan meniru browser."""
    if not os.path.exists(image_path):
        console.print(f"[bold red]Error:[/bold red] File tidak ditemukan di path '{image_path}'")
        return None

    session = requests.Session()
    session.headers.update({
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    })

    try:
        console.print("[bold cyan]Menghubungi ImgBB untuk mendapatkan token...[/bold cyan]")
        upload_page_response = session.get('https://imgbb.com/upload')
        upload_page_response.raise_for_status()

        soup = BeautifulSoup(upload_page_response.text, 'html.parser')
        auth_token_input = soup.find('input', {'name': 'auth_token'})
        
        if not auth_token_input or not auth_token_input.get('value'):
            console.print("[bold red]Gagal mendapatkan auth_token dari ImgBB.[/bold red]")
            return None
        
        auth_token = auth_token_input['value']

        console.print("[bold cyan]Token didapatkan. Mengunggah gambar...[/bold cyan]")
        
        with open(image_path, 'rb') as image_file:
            files = {'source': (os.path.basename(image_path), image_file)}
            payload = {
                'type': 'file', 'action': 'upload', 'timestamp': str(int(time.time() * 1000)),
                'auth_token': auth_token, 'expiration': 'PT5M'
            }
            upload_response = session.post('https://imgbb.com/json', files=files, data=payload)
            upload_response.raise_for_status()

        result = upload_response.json()
        
        if result.get("status_code") == 200 and result.get("success", {}).get("message") == "image uploaded":
            image_url = result["image"]["url"]
            console.print(f"[bold green]✓[/bold green] Link sementara (ImgBB): [link]{image_url}[/link]")
            return image_url
        else:
            console.print(f"[bold red]Gagal mengunggah ke ImgBB.[/bold red]")
            console.print(f"Detail error: {result.get('status_txt', 'Unknown error')}")
            return None

    except requests.exceptions.RequestException as e:
        console.print(f"[bold red]Terjadi kesalahan saat request ke ImgBB:[/bold red] {e}")
        return None
    except Exception as e:
        console.print(f"[bold red]Terjadi kesalahan tak terduga:[/bold red] {e}")
        return None

SESSIONS_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'sessions.json')

def load_sessions(chat_model: str) -> list:
    """Memuat semua sesi untuk model chat tertentu dari file JSON."""
    try:
        with open(SESSIONS_FILE, 'r') as f:
            all_sessions = json.load(f)
            return all_sessions.get(chat_model, [])
    except (FileNotFoundError, json.JSONDecodeError):
        return []

def save_all_sessions(all_sessions: dict):
    """Menyimpan semua sesi ke file JSON."""
    with open(SESSIONS_FILE, 'w') as f:
        json.dump(all_sessions, f, indent=4)

def save_new_session(chat_model: str, session_id: str, title: str):
    """Menyimpan sesi baru ke file JSON."""
    all_sessions = {}
    try:
        with open(SESSIONS_FILE, 'r') as f:
            all_sessions = json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        pass 

    if chat_model not in all_sessions:
        all_sessions[chat_model] = []
    
    if not any(s['id'] == session_id for s in all_sessions[chat_model]):
        all_sessions[chat_model].append({'id': session_id, 'title': title})
        save_all_sessions(all_sessions)

def delete_session_ui(chat_model: str):
    """Menampilkan daftar sesi dan meminta user untuk memilih yang akan dihapus."""
    sessions = load_sessions(chat_model)
    if not sessions:
        console.print("[yellow]Tidak ada sesi untuk dihapus.[/yellow]")
        cyber_input("Tekan Enter untuk kembali...")
        return

    console.print(f"\n[bold red]Pilih sesi {chat_model.upper()} yang ingin dihapus:[/bold red]")
    for i, session in enumerate(sessions):
        title = session['title'][:40] + '...' if len(session['title']) > 40 else session['title']
        console.print(f"  [bold white]{i+1}.[/bold white] {title}")
    console.print("  [bold white]0.[/bold white] Batal hapus")

    while True:
        choice = cyber_input("Masukkan nomor sesi yang akan dihapus")
        
        if choice == '0':
            console.print("[yellow]Penghapusan dibatalkan.[/yellow]")
            return
        
        if choice.isdigit() and 1 <= int(choice) <= len(sessions):
            session_to_delete = sessions[int(choice) - 1]
            confirm = cyber_input(f"Hapus sesi '{session_to_delete['title']}'? (y/n)").lower()
            if confirm == 'y':

                try:
                    with open(SESSIONS_FILE, 'r') as f:
                        all_sessions = json.load(f)
                    
                    del all_sessions[chat_model][int(choice) - 1]
                    
                    with open(SESSIONS_FILE, 'w') as f:
                        json.dump(all_sessions, f, indent=4)
                    
                    console.print("[bold green]Sesi berhasil dihapus.[/bold green]")
                except Exception as e:
                    console.print(f"[bold red]Gagal menghapus sesi: {e}[/bold red]")
            else:
                console.print("[yellow]Penghapusan dibatalkan.[/yellow]")
            return
        else:
            console.print("[red]Pilihan tidak valid.[/red]")

def display_and_select_session(chat_model: str) -> str | None:
    """Menampilkan daftar sesi dan meminta user untuk memilih atau keluar."""
    sessions = load_sessions(chat_model)
    if not sessions:
        console.print("[yellow]Tidak ada sesi tersedia. Memulai sesi baru.[/yellow]")
        return None

    console.print(f"\n[bold cyan]Pilih sesi {chat_model.upper()} yang ingin dilanjutkan:[/bold cyan]")
    for i, session in enumerate(sessions):
        title = session['title'][:40] + '...' if len(session['title']) > 40 else session['title']
        console.print(f"  [bold white]{i+1}.[/bold white] {title}")
    console.print("  [bold white]0.[/bold white] Buat sesi baru")
    console.print("  [bold red]00.[/bold red] Kembali ke menu")

    console.print("  [bold red]h.[/bold red] Hapus sesi")

    while True:
        choice = cyber_input("Masukkan nomor sesi (atau '00' untuk kembali, 'h' untuk hapus)")
        
        if choice == '00':
            return 'exit'

        if choice.lower() == 'h':
            delete_session_ui(chat_model)
            continue 
        if choice == '0':
            return None
        if choice.isdigit() and 1 <= int(choice) <= len(sessions):
            return sessions[int(choice) - 1]['id']
        console.print("[red]Pilihan tidak valid.[/red]")

def get_output_path(default_dir_name: str, filename: str) -> str:
    """
    Meminta input path output dari user atau menggunakan default.
    Membuat folder jika belum ada.
    """
    # Default path adalah 'output' di direktori yang sama dengan main.py
    project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    default_path = os.path.join(project_root, default_dir_name)
    
    # Minta input dari user, dengan default path sebagai petunjuk
    output_dir = cyber_input(f"Output path (default: {default_path})")
    
    # Jika user tidak memasukkan apa-apa, gunakan path default
    if not output_dir:
        output_dir = default_path
        
    # Pastikan folder ada
    if not os.path.exists(output_dir):
        try:
            os.makedirs(output_dir)
            console.print(f"[dim]Folder '{output_dir}' dibuat.[/dim]")
        except OSError as e:
            console.print(f"[red]Gagal membuat folder '{output_dir}': {e}[/red]")
            # Fallback ke path home/Downloads jika gagal
            output_dir = os.path.join(os.path.expanduser('~'), 'Downloads')
            if not os.path.exists(output_dir):
                 os.makedirs(output_dir)
        
    return os.path.join(output_dir, filename)