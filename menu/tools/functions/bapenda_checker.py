# menu/tools/functions/bapenda_checker.py

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

def bapenda_checker():
    """Memeriksa detail pajak kendaraan melalui BAPENDA."""
    clear()
    print_cyber_panel("Cek Pajak Kendaraan (BAPENDA)", "Periksa detail pajak kendaraan bermotor.")
    
    config = load_config()
    if not config or not config.get("base_url"):
        console.print("[bold red]Error: Konfigurasi atau base_url tidak ditemukan.[/bold red]")
        cyber_input("Tekan Enter untuk kembali...")
        return

    api_endpoint = f"{config.get('base_url')}/api/tool/cek-pajak/bapenda"
    
    plat_input = cyber_input("Masukkan nomor polisi (contoh: B1234XYZ) atau ketik '00' untuk kembali")
    
    if plat_input == '00':
        return

    try:
        with console.status("[bold green]Mengambil data pajak kendaraan...[/bold green]", spinner="dots"):
            params = {'plat': plat_input}
            response = requests.get(api_endpoint, params=params, headers={'accept': 'application/json'})
            response.raise_for_status()
            result = response.json()

        if result.get("success"):
            data = result.get("data", {})
            
            info_umum = data.get("informasi-umum", {})
            if info_umum:
                info_umum_content = [
                    Text.assemble(("Nomor Polisi:", "bold #00F0FF"), f" {info_umum.get('nomor-polisi', 'N/A')}", "white"),
                    Text.assemble(("Merk:", "bold #00F0FF"), f" {info_umum.get('merk', 'N/A')}", "white"),
                    Text.assemble(("Model:", "bold #00F0FF"), f" {info_umum.get('model', 'N/A')}", "white"),
                    Text.assemble(("Warna:", "bold #00F0FF"), f" {info_umum.get('warna', 'N/A')}", "white"),
                    Text.assemble(("Milik:", "bold #00F0FF"), f" {info_umum.get('milik-ke', 'N/A')}", "white"),
                    Text.assemble(("Jenis:", "bold #00F0FF"), f" {info_umum.get('jenis', 'N/A')}", "white"),
                    Text.assemble(("Tahun Buatan:", "bold #00F0FF"), f" {info_umum.get('tahun-buatan', 'N/A')}", "white"),
                ]
                console.print(Panel(
                    Group(*info_umum_content),
                    title="[bold magenta]🚗 Informasi Umum Kendaraan[/bold magenta]",
                    border_style="#00F0FF",
                    padding=(1, 2)
                ))

            info_pkb = data.get("informasi-pkb-pnbp", {})
            if info_pkb:
                info_pkb_content = [
                    Text.assemble(("Wilayah:", "bold #00F0FF"), f" {info_pkb.get('wilayah', 'N/A')}", "white"),
                    Text.assemble(("Masa Berlaku Pajak:", "bold #00F0FF"), f" {info_pkb.get('dari', 'N/A')} s/d {info_pkb.get('ke', 'N/A')}", "white"),
                    Text.assemble(("Tanggal Pajak:", "bold #00F0FF"), f" {info_pkb.get('tanggal-pajak', 'N/A')}", "white"),
                    Text.assemble(("Tanggal STNK:", "bold #00F0FF"), f" {info_pkb.get('tanggal-stnk', 'N/A')}", "white"),
                ]
                console.print(Panel(
                    Group(*info_pkb_content),
                    title="[bold magenta]📄 Informasi PKB & PNBP[/bold magenta]",
                    border_style="#00F0FF",
                    padding=(1, 2)
                ))

            pembayaran_pkb = data.get("pembayaran-pkb-pnbp", {})
            if pembayaran_pkb:
                pay_table = Table(show_header=True, header_style="bold #00F0FF", box=SQUARE, border_style="#00F0FF")
                pay_table.add_column("Keterangan", style="white", overflow=None)
                pay_table.add_column("Jumlah", style="white", justify="right", overflow=None)
                
                for key, value in pembayaran_pkb.items():
                    formatted_key = key.replace('-', ' ').replace('_', ' ').title()
                    pay_table.add_row(formatted_key, str(value))
                
                console.print(Panel(
                    pay_table,
                    title="[bold magenta]💳 Rincian Pembayaran PKB & PNBP[/bold magenta]",
                    border_style="#00F0FF",
                    padding=(1, 1)
                ))

            additional_info_content = [
                Text.assemble(("Tanggal Proses:", "bold #00F0FF"), f" {data.get('tanggal-proses', 'N/A')}", "white"),
                Text.assemble(("Keterangan:", "bold #00F0FF"), f" {data.get('keterangan', 'N/A')}", "white"),
                Text.assemble(("Status Pembayaran:", "bold #00F0FF"), f" {'Dapat Dibayar' if data.get('canBePaid') else 'Tidak Dapat Dibayar'}", "white"),
                Text.assemble(("Pajak 5 Tahunan:", "bold #00F0FF"), f" {'Ya' if data.get('isFiveYear') else 'Tidak'}", "white"),
            ]
            console.print(Panel(
                Group(*additional_info_content),
                title="[bold magenta]ℹ️ Informasi Tambahan[/bold magenta]",
                border_style="#00F0FF",
                padding=(1, 2)
            ))

        else:
            console.print("[bold red]Gagal mengambil data pajak kendaraan.[/bold red]")

            message = result.get("message", "Tidak ada pesan error dari server.")
            console.print(f"[bold yellow]Pesan dari Server:[/bold yellow] {message}")

            details = result.get("detail")
            if details:
                console.print("[bold yellow]Detail Error:[/bold yellow]")
                for detail in details:
                    console.print(f"- [dim]{detail}[/dim]")

            param = result.get("param")
            if param:
                param_table = Table(show_header=False, box=None)
                param_table.add_column("Key", style="bold #00F0FF")
                param_table.add_column("Value", style="white")
                for key, value in param.items():
                    param_table.add_row(key, str(value))
                console.print(Panel(param_table, title="[dim]Parameter yang Dikirim[/dim]", border_style="dim"))

    except requests.exceptions.RequestException as e:
        console.print(f"\n[bold red]Error saat menghubungi API:[/bold red] {e}")
    except Exception as e:
        console.print(f"\n[bold red]Terjadi kesalahan tak terduga:[/bold red] {e}")
        
    cyber_input("\nTekan Enter untuk kembali ke menu Tools...")