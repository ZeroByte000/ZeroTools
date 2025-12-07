# menu/tools/functions/ip_locator_checker.py

import requests
from core.utils import load_config
from app.console import console, print_cyber_panel, cyber_input, clear
from rich.panel import Panel
from rich.text import Text
from rich.console import Group
from rich.align import Align

def ip_locator_checker():
    """Memeriksa lokasi dan informasi dari alamat IP."""
    clear()
    print_cyber_panel("Ip Locator", "Cek lokasi dan informasi alamat IP.")
    
    config = load_config()
    if not config or not config.get("base_url"):
        console.print("[bold red]Error: Konfigurasi atau base_url tidak ditemukan.[/bold red]")
        cyber_input("Tekan Enter untuk kembali...")
        return

    api_endpoint = f"{config.get('base_url')}/api/tool/iplocation"
    
    ip_input = cyber_input("Masukkan alamat IP (contoh: 8.8.8.8) atau ketik '00' untuk kembali")
    
    if ip_input == '00':
        return

    try:
        with console.status("[bold green]Mengambil data lokasi IP...[/bold green]", spinner="dots"):
            params = {'ip': ip_input}
            response = requests.get(api_endpoint, params=params, headers={'accept': 'application/json'})
            response.raise_for_status()
            result = response.json()
        ip_data = result.get("ipInfo", {})
        if ip_data:

            ip_network_content = [
                Text.assemble(("Alamat IP:", "bold #00F0FF"), (f" {ip_data.get('ip', 'N/A')}", "white")),
                Text.assemble(("Jaringan:", "bold #00F0FF"), (f" {ip_data.get('network', 'N/A')}", "white")),
                Text.assemble(("Versi:", "bold #00F0FF"), (f" {ip_data.get('version', 'N/A')}", "white")),
                Text.assemble(("ASN:", "bold #00F0FF"), (f" {ip_data.get('asn', 'N/A')}", "white")),
                Text.assemble(("Organisasi:", "bold #00F0FF"), (f" {ip_data.get('org', 'N/A')}", "white")),
            ]
            console.print(Panel(
                Group(*ip_network_content),
                title="[bold magenta]🌐 Informasi IP & Jaringan[/bold magenta]",
                border_style="#00F0FF",
                padding=(1, 2)
            ))

            location_content = [
                Text.assemble(("Kota:", "bold #00F0FF"), (f" {ip_data.get('city', 'N/A')}", "white")),
                Text.assemble(("Wilayah:", "bold #00F0FF"), (f" {ip_data.get('region', 'N/A')} ({ip_data.get('region_code', 'N/A')})", "white")),
                Text.assemble(("Negara:", "bold #00F0FF"), (f" {ip_data.get('country_name', 'N/A')} ({ip_data.get('country_code', 'N/A')})", "white")),
                Text.assemble(("Kode Pos:", "bold #00F0FF"), (f" {ip_data.get('postal', 'N/A')}", "white")),
                Text.assemble(("Koordinat:", "bold #00F0FF"), (f" {ip_data.get('latitude', 'N/A')}, {ip_data.get('longitude', 'N/A')}", "white")),
                Text.assemble(("Zona Waktu:", "bold #00F0FF"), (f" {ip_data.get('timezone', 'N/A')} (UTC {ip_data.get('utc_offset', 'N/A')})", "white")),
            ]
            console.print(Panel(
                Group(*location_content),
                title="[bold magenta]📍 Informasi Lokasi[/bold magenta]",
                border_style="#00F0FF",
                padding=(1, 2)
            ))


            country_content = [
                Text.assemble(("Ibu Kota:", "bold #00F0FF"), (f" {ip_data.get('country_capital', 'N/A')}", "white")),
                Text.assemble(("Top Level Domain:", "bold #00F0FF"), (f" {ip_data.get('country_tld', 'N/A')}", "white")),
                Text.assemble(("Kode Telepon:", "bold #00F0FF"), (f" {ip_data.get('country_calling_code', 'N/A')}", "white")),
                Text.assemble(("Mata Uang:", "bold #00F0FF"), (f" {ip_data.get('currency_name', 'N/A')} ({ip_data.get('currency', 'N/A')})", "white")),
                Text.assemble(("Bahasa:", "bold #00F0FF"), (f" {ip_data.get('languages', 'N/A')}", "white")),
                Text.assemble(("Luas Area:", "bold #00F0FF"), (f" {ip_data.get('country_area', 'N/A'):,} km²", "white")),
                Text.assemble(("Populasi:", "bold #00F0FF"), (f" {ip_data.get('country_population', 'N/A'):,}", "white")),
            ]
            console.print(Panel(
                Group(*country_content),
                title="[bold magenta]🏳️ Informasi Negara[/bold magenta]",
                border_style="#00F0FF",
                padding=(1, 2)
            ))

        else:
            console.print("[bold red]Gagal mengambil data IP. 'ipInfo' tidak ditemukan dalam respons.[/bold red]")
            console.print(f"Detail: {result}")

    except requests.exceptions.RequestException as e:
        console.print(f"\n[bold red]Error saat menghubungi API:[/bold red] {e}")
    except Exception as e:
        console.print(f"\n[bold red]Terjadi kesalahan tak terduga:[/bold red] {e}")
        
    cyber_input("\nTekan Enter untuk kembali ke menu Tools...")