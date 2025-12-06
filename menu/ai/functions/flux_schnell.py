# menu/ai/functions/flux_schnell.py

import os
import requests
from datetime import datetime
from core.utils import load_config, get_output_path
from app.console import console, print_cyber_panel, cyber_input, clear, loading_animation

def flux_schnell():

    clear()
    print_cyber_panel("Flux Schnell", "Buat gambar dari deskripsi teks")

    prompt = cyber_input("Masukkan deskripsi gambar (prompt) atau ketik '00' untuk kembali")
    
    if prompt == '00':
        return
    
    if not prompt:
        console.print("[yellow]Prompt tidak boleh kosong.[/yellow]")
        cyber_input("Tekan Enter untuk kembali...")
        return

    config = load_config()
    if not config:
        cyber_input("Tekan Enter untuk kembali...")
        return
        
    base_url = config.get("base_url")
    api_endpoint = f"{base_url}/api/ai/flux-schnell"
    
    params = {
        'prompt': prompt
    }
    
    try:
        loading_animation("Membuat gambar dengan AI", duration=10)
        
        response = requests.get(api_endpoint, params=params, headers={'accept': 'image/png'})
        response.raise_for_status()

        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        output_filename = f"flux_schnell_image_{timestamp}.png"

        output_path = get_output_path("output", output_filename)
        
        with open(output_path, 'wb') as f:
            f.write(response.content)

        console.print(f"\n[bold green]✓ Gambar berhasil dibuat![/bold green]")
        console.print(f"Disimpan di: [bold cyan]{output_path}[/bold cyan]")

    except requests.exceptions.RequestException as e:
        console.print(f"\n[bold red]Error saat memanggil API:[/bold red] {e}")
    except Exception as e:
        console.print(f"\n[bold red]Terjadi kesalahan tak terduga:[/bold red] {e}")

    cyber_input("\nTekan Enter untuk kembali ke menu...")