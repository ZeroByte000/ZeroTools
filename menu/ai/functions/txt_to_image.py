# menu/ai/functions/txt_to_image.py

import os
import requests
from datetime import datetime

from core.utils import *
from app.console import *


def txt_to_image():
    """Membuat gambar dari teks (prompt) menggunakan AI."""
    clear()
    print_cyber_panel("Text to Image", "Buat gambar dari deskripsi teks")

    prompt = cyber_input("Masukkan deskripsi gambar (prompt)")
    if not prompt:
        console.print("[yellow]Prompt tidak boleh kosong.[/yellow]")
        cyber_input("Tekan Enter untuk kembali...")
        return
    while True:
        width_str = cyber_input("Lebar gambar (contoh: 512)")
        if width_str.isdigit():
            width = int(width_str)
            break
        console.print("[red]Input tidak valid. Masukkan angka.[/red]")

    while True:
        height_str = cyber_input("Tinggi gambar (contoh: 512)")
        if height_str.isdigit():
            height = int(height_str)
            break
        console.print("[red]Input tidak valid. Masukkan angka.[/red]")

    config = load_config()
    if not config:
        cyber_input("Tekan Enter untuk kembali...")
        return
        
    base_url = config.get("base_url")
    api_endpoint = f"{base_url}/api/ai/text2img"
    
    params = {
        'prompt': prompt,
        'width': width,
        'height': height
    }
    
    try:
        loading_animation("Membuat gambar dengan AI", duration=10)
        
        response = requests.get(api_endpoint, params=params, headers={'accept': 'image/png'})
        response.raise_for_status()
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        output_filename = f"anime_image_{timestamp}.png"

        # --- PERUBAHAN: Gunakan fungsi helper untuk menentukan path output ---
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