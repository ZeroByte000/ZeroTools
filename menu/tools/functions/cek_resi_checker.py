# menu/tools/functions/cek_resi_checker.py

import requests
from core.utils import load_config
from app.console import console, print_cyber_panel, cyber_input, clear
from rich.table import Table
from rich.panel import Panel
from rich.text import Text
from rich.console import Group
from rich.align import Align
from rich.box import SQUARE

def get_courier_choice():
    """Menampilkan daftar ekspedisi dan mengembalikan pilihan pengguna."""
    # Daftar ekspedisi yang didukung
    couriers = [
        {"name": "ACOMMERCE", "code": "acommerce"},
        {"name": "Anter Aja", "code": "anter-aja"},
        {"name": "Ark Xpress", "code": "ark-xpress"},
        {"name": "Grab Express", "code": "grab-express"},
        {"name": "GTL Goto Logistics", "code": "gtl-goto-logistics"},
        {"name": "Indah Logistik Cargo", "code": "indah-logistik-cargo"},
        {"name": "Janio Asia", "code": "janio-asia"},
        {"name": "Jet Express", "code": "jet-express"},
        {"name": "Lion Parcel", "code": "lion-parcel"},
        {"name": "Luar Negeri (Bea Cukai)", "code": "luar-negeri-bea-cukai"},
        {"name": "Lazada Express (LEX)", "code": "lazada-express-lex"},
        {"name": "Lazada Logistics", "code": "lazada-logistics"},
        {"name": "Ninja Xpress", "code": "ninja"},
        {"name": "NSS Express", "code": "nss-express"},
        {"name": "Paxel", "code": "paxel"},
        {"name": "PCP Express", "code": "pcp-express"},
        {"name": "POS Indonesia", "code": "pos-indonesia"},
        {"name": "PT NCS", "code": "pt-ncs"},
        {"name": "QRIM Express", "code": "qrim-express"},
        {"name": "RCL Red Carpet Logistics", "code": "rcl-red-carpet-logistics"},
        {"name": "SAP Express", "code": "sap-express"},
        {"name": "Shopee Express", "code": "shopee-express"},
        {"name": "Standard Express LWE", "code": "standard-express-lwe"},
        {"name": "TIKI", "code": "tiki"},
    ]

    while True:
        clear()
        table = Table(
            show_header=True,
            header_style="bold #00F0FF",
            title="[bold magenta]🚚 Pilih Ekspedisi 🚚[/bold magenta]",
            title_style="bold magenta",
            title_justify="center",
            box=SQUARE,
            border_style="#00F0FF",
            show_lines=True,
            padding=(0, 1)
        )
        table.add_column("No.", style="bold white", width=4, justify="center")
        table.add_column("Ekspedisi", style="bold white", overflow=None)

        for i, courier in enumerate(couriers):
            table.add_row(str(i + 1), courier['name'])
        
        table.add_row("0", "[bold yellow]← Kembali[/bold yellow]")

        panel = Panel(
            table,
            border_style="#00F0FF",
            padding=(1, 1)
        )
        console.print(panel)

        choice = cyber_input("Pilih ekspedisi")

        if choice in ['0', 'b']:
            return None, None 
        
        if choice.isdigit() and 1 <= int(choice) <= len(couriers):
            selected_courier = couriers[int(choice) - 1]
            return selected_courier['name'], selected_courier['code']
        
        console.print("[bold red]Pilihan tidak valid![/bold red]")
        cyber_input("Tekan Enter untuk mencoba lagi...")

def cek_resi_checker():
    """Memeriksa status pengiriman paket (resi)."""
    clear()
    print_cyber_panel("Cek Resi", "Lacak paket dari berbagai ekspedisi.")
    
    config = load_config()
    if not config or not config.get("base_url"):
        console.print("[bold red]Error: Konfigurasi atau base_url tidak ditemukan.[/bold red]")
        cyber_input("Tekan Enter untuk kembali...")
        return

    courier_name, courier_code = get_courier_choice()
    if courier_code is None:
        return

    api_endpoint = f"{config.get('base_url')}/api/tool/cek-resi"
    
    resi_input = cyber_input(f"Masukkan nomor resi untuk [bold cyan]{courier_name}[/bold cyan] atau ketik '00' untuk kembali")
    
    if resi_input == '00':
        return

    try:
        with console.status("[bold green]Mengambil data resi...[/bold green]", spinner="dots"):
            params = {'resi': resi_input, 'ekspedisi': courier_code}
            response = requests.get(api_endpoint, params=params, headers={'accept': 'application/json'})
            response.raise_for_status()
            result = response.json()

        if result.get("success"):
            data = result.get("data", {})

            info_content = [
                Text.assemble(("No. Resi:", "bold #00F0FF"), (f" {data.get('resi', 'N/A')}", "white")),
                Text.assemble(("Ekspedisi:", "bold #00F0FF"), (f" {data.get('ekspedisi', 'N/A')}", "white")),
                Text.assemble(("Status:", "bold #00F0FF"), (f" {data.get('status', 'N/A')}", "white")),
                Text.assemble(("Tanggal Kirim:", "bold #00F0FF"), (f" {data.get('tanggalKirim', 'N/A')}", "white")),
                Text.assemble(("CS:", "bold #00F0FF"), (f" {data.get('customerService', 'N/A')}", "white")),
                Text.assemble(("Posisi Terakhir:", "bold #00F0FF"), (f" {data.get('lastPosition', 'N/A')}", "white")),
            ]
            console.print(Panel(
                Group(*info_content),
                title="[bold magenta]📦 Informasi Pengiriman[/bold magenta]",
                border_style="#00F0FF",
                padding=(1, 2)
            ))

            history = data.get("history", [])
            if history:
                history_panels = []
                for item in history:
                    content = [
                        Text.assemble(("Tanggal: ", "bold #00F0FF"), (item.get('tanggal', 'N/A'), "white")),
                        Text.assemble(("Keterangan: ", "bold #00F0FF"), (item.get('keterangan', 'N/A'), "white"))
                    ]
                    history_panel = Panel(
                        Group(*content),
                        box=SQUARE, 
                        border_style="dim", 
                        padding=(0, 1)
                    )
                    history_panels.append(history_panel)

                console.print(Panel(
                    Group(*history_panels),
                    title="[bold magenta]📍 Riwayat Perjalanan[/bold magenta]",
                    border_style="#00F0FF",
                    padding=(1, 1)
                ))
            else:
                console.print(Panel("[dim]Tidak ada riwayat perjalanan ditemukan.[/dim]", title="[bold magenta]📍 Riwayat Perjalanan[/bold magenta]", border_style="#00F0FF"))

        else:
            console.print("[bold red]Gagal mengambil data resi.[/bold red]")
            message = result.get("message", "Tidak ada pesan error dari server.")
            console.print(f"[bold yellow]Pesan dari Server:[/bold yellow] {message}")

    except requests.exceptions.RequestException as e:
        console.print(f"\n[bold red]Error saat menghubungi API:[/bold red] {e}")
    except Exception as e:
        console.print(f"\n[bold red]Terjadi kesalahan tak terduga:[/bold red] {e}")
        
    cyber_input("\nTekan Enter untuk kembali ke menu Tools...")