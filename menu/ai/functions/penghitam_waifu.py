# menu/ai/functions/penghitam_waifu.py

import os
import requests
from datetime import datetime

from core.utils import *
from app.console import *

def penghitam_waifu():
    clear()
    print_cyber_panel("Penghitam Waifu", "Masukkan path gambar atau link URL")
    image_input = cyber_input("Path/URL gambar (contoh: /sdcard/foto.jpg) atau ketik '00' untuk kembali")
    if image_input == '00':
        return

    public_url = None

    if image_input.startswith(('http://', 'https://')):
        console.print("[bold cyan]Mendeteksi input berupa URL...[/bold cyan]")
        public_url = image_input
    else:
        console.print("[bold cyan]Mendeteksi input berupa path file lokal...[/bold cyan]")
        if not os.path.exists(image_input):
            console.print(f"[bold red]Error:[/bold red] File tidak ditemukan di path '{image_input}'")
            cyber_input("Tekan Enter untuk kembali...")
            return

        public_url = upload_to_imgbb_no_api(image_path=image_input)
        
        if not public_url:
            cyber_input("Tekan Enter untuk kembali...")
            return

    if public_url:
        config = load_config()
        if not config:
            cyber_input("Tekan Enter untuk kembali...")
            return
            
        base_url = config.get("base_url")
        api_endpoint = f"{base_url}/api/ai/negro"
        
        params = {
            'url': public_url
        }
        
        try:
            loading_animation("Memproses gambar dengan AI", duration=5)
            
            response = requests.get(api_endpoint, params=params, headers={'accept': 'image/png'})
            response.raise_for_status()

            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            output_filename = f"anime_image_{timestamp}.png"
            output_path = get_output_path("output", output_filename)

            with open(output_path, 'wb') as f:
                f.write(response.content)
                
            console.print(f"\n[bold green]✓ Gambar berhasil diubah![/bold green]")
            console.print(f"Disimpan di: [bold cyan]{output_path}[/bold cyan]")

        except requests.exceptions.RequestException as e:
            console.print(f"\n[bold red]Error saat memanggil API:[/bold red] {e}")
        except Exception as e:
            console.print(f"\n[bold red]Terjadi kesalahan tak terduga:[/bold red] {e}")
 
    cyber_input("\nTekan Enter untuk kembali ke menu...")