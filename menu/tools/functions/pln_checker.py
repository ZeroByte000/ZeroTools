# menu/tools/functions/pln_checker.py

import requests
import json
from core.utils import load_config
from app.console import console, print_cyber_panel, cyber_input, clear
from rich.panel import Panel
from rich.text import Text
from rich.console import Group
from rich.align import Align

def pln_checker():
    """Memeriksa detail dan tagihan listrik PLN."""
    clear()
    print_cyber_panel("Cek PLN", "Periksa detail dan tagihan listrik PLN.")
    
    config = load_config()
    if not config or not config.get("base_url"):
        console.print("[bold red]Error: Konfigurasi atau base_url tidak ditemukan.[/bold red]")
        cyber_input("Tekan Enter untuk kembali...")
        return

    api_endpoint = f"{config.get('base_url')}/api/tool/cek-pln"
    
    id_input = cyber_input("Masukkan ID Pelanggan (contoh: 5xxxxxxxxx) atau ketik '00' untuk kembali")
    
    if id_input == '00':
        return

    try:
        with console.status("[bold green]Mengambil data PLN...[/bold green]", spinner="dots"):
            params = {'id': id_input}
            response = requests.get(api_endpoint, params=params, headers={'accept': 'application/json'})
            response.raise_for_status()
            result = response.json()

        if result.get("success"):
            data = result.get("result", {})
            
            info_content = [
                Text.assemble(("ID Pelanggan:", "bold #00F0FF"), (f" {data.get('customer_id', 'N/A')}", "white")),
                Text.assemble(("Nama Pelanggan:", "bold #00F0FF"), (f" {data.get('customer_name', 'N/A')}", "white")),
                Text.assemble(("Tagihan Outstanding:", "bold #00F0FF"), (f" {data.get('outstanding_balance', 'N/A')}", "white")),
                Text.assemble(("Periode Tagihan:", "bold #00F0FF"), (f" {data.get('billing_period', 'N/A')}", "white")),
                Text.assemble(("Bacaan Meter:", "bold #00F0FF"), (f" {data.get('meter_reading', 'N/A')}", "white")),
                Text.assemble(("Daya / Golongan:", "bold #00F0FF"), (f" {data.get('power_category', 'N/A')}", "white")),
                Text.assemble(("Jumlah Tagihan:", "bold #00F0FF"), (f" {data.get('total_bills', 'N/A')}", "white")),
            ]
            console.print(Panel(
                Group(*info_content),
                title="[bold magenta]⚡ Informasi PLN[/bold magenta]",
                border_style="#00F0FF",
                padding=(1, 2)
            ))

        else:
            console.print("[bold red]Gagal mengambil data PLN.[/bold red]")
            message = result.get("message", "Tidak ada pesan error dari server.")
            console.print(f"[bold yellow]Pesan dari Server:[/bold yellow] {message}")

    except requests.exceptions.RequestException as e:
        console.print(f"\n[bold red]Error saat menghubungi API:[/bold red] {e}")
    except Exception as e:
        console.print(f"\n[bold red]Terjadi kesalahan tak terduga:[/bold red] {e}")
        
    cyber_input("\nTekan Enter untuk kembali ke menu Tools...")