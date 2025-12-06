# menu/uploader/functions/image_db_uploader.py

import os
import requests
import json
from datetime import datetime
import time
from bs4 import BeautifulSoup
from core.utils import load_config, get_output_path, get_expiration
from app.console import console, print_cyber_panel, cyber_input, clear, loading_animation

def upload_to_imgbb(image_path: str, expiration: str = "") -> str | None:
    if not os.path.exists(image_path):
        return None

    session = requests.Session()
    session.headers.update({
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    })

    try:

        upload_page_response = session.get('https://imgbb.com/upload')
        upload_page_response.raise_for_status()

        soup = BeautifulSoup(upload_page_response.text, 'html.parser')
        auth_token_input = soup.find('input', {'name': 'auth_token'})
        
        if not auth_token_input or not auth_token_input.get('value'):
            return None
        
        auth_token = auth_token_input['value']
        
        with open(image_path, 'rb') as image_file:
            files = {'source': (os.path.basename(image_path), image_file)}
            payload = {
                'type': 'file', 
                'action': 'upload', 
                'timestamp': str(int(time.time() * 1000)),
                'auth_token': auth_token
            }
            
            if expiration:
                payload['expiration'] = expiration
            
            upload_response = session.post('https://imgbb.com/json', files=files, data=payload)
            upload_response.raise_for_status()

        result = upload_response.json()
        
        if result.get("status_code") == 200 and result.get("success", {}).get("message") == "image uploaded":
            return result["image"]["url"]
        else:
            return None 

    except requests.exceptions.RequestException:
        return None 
    except Exception:
        return None 

def image_db_uploader():
    clear()
    print_cyber_panel("Image DB Uploader", "Unggah gambar ke ImgBB")
    
    image_input = cyber_input("Path gambar (contoh: /sdcard/foto.jpg) atau ketik '00' untuk kembali")
    
    if image_input == '00':
        return

    if not os.path.exists(image_input):
        console.print(f"[bold red]Error:[/bold red] File tidak ditemukan di path '{image_input}'")
        cyber_input("Tekan Enter untuk kembali...")
        return

    expiration = get_expiration()

    result_url = None
    try:
        with console.status("[bold green]Menghubungi ImgBB dan mengunggah gambar...[/bold green]", spinner="dots"):
            result_url = upload_to_imgbb(image_input, expiration)

        if result_url:
            console.print(f"\n[bold green]✓ Gambar berhasil diunggah![/bold green]")
            console.print(f"[bold cyan]URL:[/bold cyan] {result_url}")

            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            log_filename = f"imgbb_upload_log_{timestamp}.json"

            log_path = get_output_path("output", log_filename)
            
            log_data = {
                "url": result_url,
                "image_path": image_input,
                "expiration": expiration,
                "timestamp": timestamp
            }
            
            with open(log_path, 'w') as f:
                json.dump(log_data, f, indent=4)
            
            console.print(f"[dim]Log respons disimpan di: {log_path}[/dim]")
        else:
            console.print(f"\n[bold red]Gagal mengunggah gambar ke ImgBB.[/bold red]")
            console.print("[yellow]Pastikan koneksi internet stabil dan coba lagi.[/yellow]")

    except Exception as e:
        console.print(f"\n[bold red]Terjadi kesalahan tak terduga:[/bold red] {e}")
        
    cyber_input("\nTekan Enter untuk kembali ke menu...")