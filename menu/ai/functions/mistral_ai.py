# menu/ai/functions/mistral_ai.py

import requests
from core.utils import load_config, display_and_select_session, save_new_session
from app.console import console, print_cyber_panel, cyber_input, clear
from rich.panel import Panel
from rich.align import Align

def mistral_ai():
    clear()
    print_cyber_panel("Mistral AI Chat", "Kelola sesi percakapan Anda.")
    
    config = load_config()
    if not config:
        cyber_input("Tekan Enter untuk kembali...")
        return
        
    base_url = config.get("base_url")
    api_endpoint = f"{base_url}/api/ai/mistral"
    
    session_id = display_and_select_session('mistral')
    
    if session_id == 'exit':
        return

    is_new_session = session_id is None

    if is_new_session:
        console.print("[bold green]Memulai sesi baru...[/bold green]")
    else:
        console.print(f"[bold green]Melanjutkan sesi lama...[/bold green]")

    while True:
        user_message = cyber_input("Anda (ketik 'keluar' untuk keluar dari chat)")
        
        if user_message.lower() in ['keluar', 'exit', 'quit']:
            console.print("[bold yellow]Mengakhiri sesi chat...[/bold yellow]")
            break
        
        if not user_message:
            console.print("[dim]Pesan tidak boleh kosong.[/dim]")
            continue
        user_panel = Panel(
            user_message,
            title="[bold blue]Anda[/bold blue]",
            border_style="blue",
            padding=(0, 1)
        )
        console.print(Align.right(user_panel))

        try:
            with console.status("[bold green]Mistral sedang mengetik...[/bold green]", spinner="dots"):
                params = {'text': user_message}
                if session_id:
                    params['session'] = session_id
                
                response = requests.get(api_endpoint, params=params, headers={'accept': 'application/json'})
                response.raise_for_status()
                data = response.json()

            if data.get("success"):
                ai_reply = data.get("result")
                session_id = data.get("session")
                
                if is_new_session:
                    save_new_session('mistral', session_id, user_message)
                    is_new_session = False

                ai_panel = Panel(
                    ai_reply,
                    title="[bold #00F0FF]Mistral AI[/bold #00F0FF]",
                    border_style="#00F0FF",
                    padding=(0, 1)
                )
                console.print(Align.left(ai_panel))
            else:
                console.print(f"[bold red]Gagal mendapatkan respons dari AI.[/bold red]")
                console.print(f"Detail: {data}")

        except requests.exceptions.RequestException as e:
            console.print(f"\n[bold red]Error saat menghubungi API:[/bold red] {e}")
        except Exception as e:
            console.print(f"\n[bold red]Terjadi kesalahan tak terduga:[/bold red] {e}")

    cyber_input("\nTekan Enter untuk kembali ke menu...")