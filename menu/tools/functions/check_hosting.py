# menu/tools/functions/check_hosting.py

import requests
import json
from core.utils import load_config
from app.console import console, print_cyber_panel, cyber_input, clear
from rich.table import Table
from rich.panel import Panel
from rich.text import Text
from rich.console import Group
from rich.align import Align
from rich.box import SQUARE

def check_hosting():
    """Memeriksa informasi hosting dan DNS untuk sebuah domain."""
    clear()
    print_cyber_panel("Cek Hosting", "Periksa informasi hosting dan DNS domain.")
    
    config = load_config()
    if not config:
        cyber_input("Tekan Enter untuk kembali...")
        return
        
    base_url = config.get("base_url")
    if not base_url:
        console.print("[bold red]Error: base_url tidak ditemukan dalam konfigurasi.[/bold red]")
        cyber_input("Tekan Enter untuk kembali...")
        return

    api_endpoint = f"{base_url}/api/tool/check-hosting"
    
    domain_input = cyber_input("Masukkan domain (contoh: google.com) atau ketik '00' untuk kembali")
    
    if domain_input == '00':
        return

    try:
        with console.status("[bold green]Mengambil informasi hosting...[/bold green]", spinner="dots"):
            params = {'domain': domain_input}
            response = requests.get(api_endpoint, params=params, headers={'accept': 'application/json'})
            response.raise_for_status()
            result = response.json()

        if result.get("success"):
            data = result.get("result", {})
            
            domain_info = data.get("domain", {})
            domain_panel_content = [
                Text.assemble(("Nama Domain: ", "bold #00F0FF"), (domain_info.get("name", "N/A"), "white")),
                Text.assemble(("Asli: ", "bold #00F0FF"), (domain_info.get("original", "N/A"), "white")),
                Text.assemble(("Dukungan IPv6: ", "bold #00F0FF"), ("Ya" if domain_info.get("ipv6_support") else "Tidak", "white")),
            ]
            console.print(Panel(
                Group(*domain_panel_content),
                title="[bold magenta]📡 Informasi Domain[/bold magenta]",
                border_style="#00F0FF",
                padding=(1, 2)
            ))

            web_info = data.get("web", {})
            if web_info.get("ips"):
                web_table = Table(show_header=True, header_style="bold #00F0FF", box=SQUARE, border_style="#00F0FF")
                web_table.add_column("IP Address", style="white", justify="left", overflow=None)
                web_table.add_column("Tipe", style="white", justify="center", overflow=None)
                web_table.add_column("Lokasi", style="white", justify="left", overflow=None)
                web_table.add_column("Provider", style="white", justify="left", overflow=None)

                for ip_info in web_info.get("ips"):
                    ip = ip_info.get("address", "N/A")
                    ip_type = "IPv6" if ip_info.get("is_ipv6") else "IPv4"
                    location = ip_info.get("location", {})
                    loc_str = f"{location.get('city', 'N/A')}, {location.get('country', 'N/A')}"
                    provider = ip_info.get("provider", {})
                    prov_str = f"{provider.get('organization', 'N/A')} ({provider.get('domain', 'N/A')})"
                    web_table.add_row(ip, ip_type, loc_str, prov_str)
                
                console.print(Panel(
                    web_table,
                    title="[bold magenta]🌐 Web Server[/bold magenta]",
                    border_style="#00F0FF",
                    padding=(1, 1)
                ))
            else:
                console.print(Panel("[dim]Tidak ada informasi Web Server yang ditemukan.[/dim]", title="[bold magenta]🌐 Web Server[/bold magenta]", border_style="#00F0FF"))

            ns_info = data.get("nameserver", {})
            if ns_info.get("servers"):
                ns_table = Table(show_header=True, header_style="bold #00F0FF", box=SQUARE, border_style="#00F0FF")
                ns_table.add_column("Domain Nameserver", style="white", justify="left", overflow=None)
                ns_table.add_column("IP Address", style="white", justify="left", overflow=None)
                ns_table.add_column("Lokasi", style="white", justify="left", overflow=None)
                
                for server in ns_info.get("servers"):
                    ns_domain = server.get("domain", "N/A")
                    for ip_info in server.get("ips", []):
                        ip = ip_info.get("address", "N/A")
                        location = ip_info.get("location", {})
                        loc_str = f"{location.get('city', 'N/A')}, {location.get('country', 'N/A')}"
                        ns_table.add_row(ns_domain, ip, loc_str)
                
                console.print(Panel(
                    ns_table,
                    title="[bold magenta]🔧 Nameserver[/bold magenta]",
                    border_style="#00F0FF",
                    padding=(1, 1)
                ))
            else:
                console.print(Panel("[dim]Tidak ada informasi Nameserver yang ditemukan.[/dim]", title="[bold magenta]🔧 Nameserver[/bold magenta]", border_style="#00F0FF"))

            mail_info = data.get("mail", {})
            incoming_servers = mail_info.get("incoming", {}).get("servers", [])
            outgoing_servers = mail_info.get("outgoing", {}).get("servers", [])

            if incoming_servers or outgoing_servers:
                if incoming_servers:
                    mail_table = Table(show_header=True, header_style="bold #00F0FF", box=SQUARE, border_style="#00F0FF")
                    mail_table.add_column("Server", style="white", justify="left", overflow=None)
                    mail_table.add_column("Lokasi", style="white", justify="left", overflow=None)
                    for server in incoming_servers:
                        loc = server.get("location", {})
                        loc_str = f"{loc.get('city', 'N/A')}, {loc.get('country', 'N/A')}"
                        mail_table.add_row(server.get("domain", "N/A"), loc_str)
                    console.print(Panel(mail_table, title="[bold magenta]📧 Mail Server (Incoming)[/bold magenta]", border_style="#00F0FF", padding=(1,1)))

                if outgoing_servers:
                    mail_table = Table(show_header=True, header_style="bold #00F0FF", box=SQUARE, border_style="#00F0FF")
                    mail_table.add_column("Server", style="white", justify="left", overflow=None)
                    mail_table.add_column("Lokasi", style="white", justify="left", overflow=None)
                    for server in outgoing_servers:
                        loc = server.get("location", {})
                        loc_str = f"{loc.get('city', 'N/A')}, {loc.get('country', 'N/A')}"
                        mail_table.add_row(server.get("domain", "N/A"), loc_str)
                    console.print(Panel(mail_table, title="[bold magenta]📧 Mail Server (Outgoing)[/bold magenta]", border_style="#00F0FF", padding=(1,1)))
            else:
                console.print(Panel("[dim]Tidak ada informasi Mail Server yang ditemukan.[/dim]", title="[bold magenta]📧 Mail Server[/bold magenta]", border_style="#00F0FF"))

            timestamp = data.get("timestamp", "N/A")
            console.print(Panel(
                Text.assemble(("Timestamp: ", "bold #00F0FF"), (timestamp, "white")),
                border_style="#00F0FF",
                padding=(0, 2)
            ))

        else:
            console.print(f"[bold red]Gagal mengambil informasi hosting.[/bold red]")
            console.print(f"Detail: {result}")

    except requests.exceptions.RequestException as e:
        console.print(f"\n[bold red]Error saat menghubungi API:[/bold red] {e}")
    except Exception as e:
        console.print(f"\n[bold red]Terjadi kesalahan tak terduga:[/bold red] {e}")
        
    cyber_input("\nTekan Enter untuk kembali ke menu Tools...")