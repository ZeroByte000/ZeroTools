# menu/ai/functions/chatgpt_v2.py

import requests
import os
from core.utils import *
from app.console import *

def chatgpt_v2():
    """Memulai sesi chat dengan ChatGPT V2 (dengan analisis gambar)."""
    clear()
    print_cyber_panel("ChatGPT V2 Chat", "Kelola sesi percakapan Anda (dapat menganalisis gambar).")
    
    config = load_config()
    if not config:
        cyber_input("Tekan Enter untuk kembali...")
        return
        
    base_url = config.get("base_url")
    api_endpoint = f"{base_url}/api/ai/v2/chatgpt"
    
    session_id = display_and_select_session('chatgptv2')
    
    if session_id == 'exit':
        return

    is_new_session = session_id is None

    if is_new_session:
        console.print("[bold green]Memulai sesi baru...[/bold green]")
    else:
        console.print(f"[bold green]Melanjutkan sesi lama...[/bold green]")

    while True:
        user_message = cyber_input("Anda")
        
        if user_message.lower() in ['keluar', 'exit', 'quit']:
            console.print("[bold yellow]Mengakhiri sesi chat...[/bold yellow]")
            break
        
        if not user_message:
            console.print("[dim]Pesan tidak boleh kosong.[/dim]")
            continue
        include_image = cyber_input("Apakah ingin menyertakan gambar? (y/n)").lower()
        image_url = None

        if include_image == 'y':
            image_input = cyber_input("Masukkan path/URL gambar:")
            
            if image_input.startswith(('http://', 'https://')):
                console.print("[bold cyan]Menggunakan URL gambar...[/bold cyan]")
                image_url = image_input
            else:
                console.print("[bold cyan]Mengunggah gambar lokal...[/bold cyan]")
                if not os.path.exists(image_input):
                    console.print(f"[bold red]Error:[/bold red] File tidak ditemukan di path '{image_input}'")
                    cyber_input("Tekan Enter untuk melanjutkan...")
                    continue 
                image_url = upload_to_imgbb_no_api(image_path=image_input)
                if not image_url:
                    console.print("[bold red]Gagal mengunggah gambar. Pesan akan dikirim tanpa gambar.[/bold red]")
        
        try:
            with console.status("[bold green]ChatGPT V2 sedang berpikir...[/bold green]", spinner="dots"):
                params = {'text': user_message}
                if session_id:
                    params['session'] = session_id
                if image_url:
                    params['imageUrl'] = image_url
                
                response = requests.get(api_endpoint, params=params, headers={'accept': 'application/json'})
                response.raise_for_status()
                data = response.json()

            if data.get("success"):
                ai_reply = data.get("result")
                session_id = data.get("session")
                
                if is_new_session:
                    save_new_session('chatgptv2', session_id, user_message)
                    is_new_session = False
                
                console.print(f"\n[bold green]AI:[/bold green] {ai_reply}\n")
            else:
                console.print(f"[bold red]Gagal mendapatkan respons dari AI.[/bold red]")
                console.print(f"Detail: {data}")

        except requests.exceptions.RequestException as e:
            console.print(f"\n[bold red]Error saat menghubungi API:[/bold red] {e}")
        except Exception as e:
            console.print(f"\n[bold red]Terjadi kesalahan tak terduga:[/bold red] {e}")

    cyber_input("\nTekan Enter untuk kembali ke menu...")