# menu/tools/main.py

from .functions.check_hosting import check_hosting
from .functions.bapenda_checker import bapenda_checker
from app.console import console, cyber_input, clear
from .functions.pln_checker import pln_checker
from .functions.cek_resi_checker import cek_resi_checker
from .functions.ip_locator_checker import ip_locator_checker
from rich.table import Table
from rich.panel import Panel
from rich.box import SQUARE


def main():
    """Fungsi utama untuk menu Tools."""
    menu_actions = {
        '1': check_hosting,
        '2': bapenda_checker,
        '3': pln_checker,
        '4': cek_resi_checker,
        '5': ip_locator_checker,
    }

    while True:
        clear()
        
        table = Table(
            show_header=True,
            header_style="bold #00F0FF",
            title="[bold magenta]🔧 Tools 🔧[/bold magenta]",
            title_style="bold magenta",
            title_justify="center",
            box=SQUARE,
            border_style="#00F0FF",
            show_lines=True,
            padding=(0, 1)
        )
        table.add_column("No.", style="bold white", width=4, justify="center")
        table.add_column("Menu", style="bold white", overflow=None)
        table.add_column("Deskripsi", style="bold white", overflow=None)

        tools_options = [
            {"name": "Cek Hosting", "desc": "Periksa informasi hosting dan DNS domain."},
            {"name": "Bapenda", "desc": "Cek detail Pajak Kendaraan Bermotor."},
            {"name": "Cek PLN", "desc": "Cek detail dan tagihan listrik PLN."},
            {"name": "Cek Resi", "desc": "Lacak paket dari berbagai ekspedisi."},
            {"name": "Ip Locator", "desc": "Cek lokasi dan informasi alamat IP."},
        ]
        
        for i, item in enumerate(tools_options):
            table.add_row(
                str(i + 1),
                item['name'],
                item['desc']
            )
        
        table.add_row("0", "[bold yellow]← Kembali[/bold yellow]", "[bold #00F0FF]Kembali ke menu utama.[/bold #00F0FF]")

        panel = Panel(
            table,
            border_style="#00F0FF",  
            padding=(1, 1)
        )
        console.print(panel)

        console.print("[dim]Gunakan '0' atau 'b' untuk kembali.[/dim]")

        choice = cyber_input("Pilih alat Tools")

        if choice in menu_actions:
            menu_actions[choice]()
        elif choice in ['0', 'b']:
            break  
        else:
            console.print("[bold red]Pilihan tidak valid![/bold red]")
            cyber_input("Tekan Enter untuk melanjutkan...")