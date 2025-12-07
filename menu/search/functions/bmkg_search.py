import requests
from datetime import datetime

# Import fungsi konfigurasi dan console
from core.utils import load_config
from app.console import console, print_cyber_panel, cyber_input, clear

# Import komponen Rich
from rich.panel import Panel
from rich.text import Text
from rich.console import Group
from rich.table import Table
from rich.box import SQUARE

def get_bmkg_data(config):
    """Mengambil data dari API BMKG."""
    try:
        api_endpoint = f"{config.get('base_url')}/api/search/bmkg"
        with console.status("[bold green]Mengambil data dari BMKG...[/bold green]", spinner="dots"):
            response = requests.get(api_endpoint, headers={'accept': 'application/json'})
            response.raise_for_status()
            return response.json()
    except requests.exceptions.RequestException as e:
        console.print(f"\n[bold red]Error saat menghubungi API:[/bold red] {e}")
        return None
    except Exception as e:
        console.print(f"\n[bold red]Terjadi kesalahan tak terduga:[/bold red] {e}")
        return None

def display_autogempa(data):
    """Menampilkan informasi gempa otomatis."""
    clear()
    if not data:
        console.print("[bold red]Data gempa otomatis tidak tersedia.[/bold red]")
        cyber_input("Tekan Enter untuk kembali...")
        return

    info_items = [
        Text.assemble(("Tanggal & Jam: ", "bold #00F0FF"), (f"{data.get('Tanggal', 'N/A')} - {data.get('Jam', 'N/A')}", "white")),
        Text.assemble(("Koordinat: ", "bold #00F0FF"), (data.get('Coordinates', 'N/A'), "white")),
        Text.assemble(("Lintang & Bujur: ", "bold #00F0FF"), (f"{data.get('Lintang', 'N/A')}, {data.get('Bujur', 'N/A')}", "white")),
        Text.assemble(("Magnitudo: ", "bold #00F0FF"), (data.get('Magnitude', 'N/A'), "white")),
        Text.assemble(("Kedalaman: ", "bold #00F0FF"), (data.get('Kedalaman', 'N/A'), "white")),
        Text.assemble(("Wilayah: ", "bold #00F0FF"), (data.get('Wilayah', 'N/A'), "white")),
        Text.assemble(("Potensi Tsunami: ", "bold #00F0FF"), (data.get('Potensi', 'N/A'), "white")),
        Text.assemble(("Dirasakan: ", "bold #00F0FF"), (data.get('Dirasakan', 'N/A'), "white")),
    ]

    info_group = Group(*info_items)
    
    panel = Panel(
        info_group,
        title="[bold magenta]🌋 Gempa Otomatis Terkini 🌋[/bold magenta]",
        border_style="medium_purple",
        padding=(1, 2)
    )
    console.print(panel)
    cyber_input("Tekan Enter untuk kembali ke menu BMKG...")

def display_gempa_list(data_list, title):
    """Menampilkan daftar gempa (terkini atau dirasakan) tanpa tabel."""
    clear()
    if not data_list:
        console.print("[bold red]Tidak ada data gempa.[/bold red]")
        cyber_input("Tekan Enter untuk kembali...")
        return

    gempa_panels = []
    
    for i, gempa in enumerate(data_list):
        gempa_info = [
            Text.assemble((f"{i+1}. ", "bold cyan")),
            Text.assemble(("Tanggal: ", "bold #00F0FF"), (gempa.get('Tanggal', 'N/A'), "white")),
            Text.assemble(("Jam: ", "bold #00F0FF"), (gempa.get('Jam', 'N/A'), "white")),
            Text.assemble(("Koordinat: ", "bold #00F0FF"), (gempa.get('Coordinates', 'N/A'), "white")),
            Text.assemble(("Lintang & Bujur: ", "bold #00F0FF"), (f"{gempa.get('Lintang', 'N/A')}, {gempa.get('Bujur', 'N/A')}", "white")),
            Text.assemble(("Magnitudo: ", "bold #00F0FF"), (gempa.get('Magnitude', 'N/A'), "white")),
            Text.assemble(("Kedalaman: ", "bold #00F0FF"), (gempa.get('Kedalaman', 'N/A'), "white")),
            Text.assemble(("Wilayah: ", "bold #00F0FF"), (gempa.get('Wilayah', 'N/A'), "white")),
        ]
        
        # Tambahkan informasi tambahan jika ada
        if 'Potensi' in gempa:
            gempa_info.append(Text.assemble(("Potensi Tsunami: ", "bold #00F0FF"), (gempa.get('Potensi', 'N/A'), "white")))
        
        if 'Dirasakan' in gempa:
            gempa_info.append(Text.assemble(("Dirasakan: ", "bold #00F0FF"), (gempa.get('Dirasakan', 'N/A'), "white")))
        
        gempa_panel = Panel(
            Group(*gempa_info),
            border_style="medium_purple",
            padding=(0, 1)
        )
        gempa_panels.append(gempa_panel)

    main_panel = Panel(
        Group(*gempa_panels),
        title=title,
        border_style="#00F0FF",
        padding=(1, 1)
    )
    console.print(main_panel)
    cyber_input("Tekan Enter untuk kembali ke menu BMKG...")

def bmkg_search():
    """Menampilkan informasi gempa dari BMKG."""
    clear()
    print_cyber_panel("BMKG Info", "Informasi Gempa Terkini dari Badan Meteorologi, Klimatologi, dan Geofisika.")
    
    config = load_config()
    if not config or not config.get("base_url"):
        console.print("[bold red]Error: Konfigurasi atau base_url tidak ditemukan.[/bold red]")
        cyber_input("Tekan Enter untuk kembali...")
        return

    while True:
        clear()
        table = Table(
            show_header=True,
            header_style="bold #00F0FF",
            title="[bold magenta]🌋 Menu Informasi Gempa BMKG 🌋[/bold magenta]",
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

        menu_options = [
            {"name": "Gempa Terkini", "desc": "Daftar gempa bumi terkini dengan magnitudo > 5.0."},
            {"name": "Gempa Dirasakan", "desc": "Daftar gempa bumi yang dirasakan masyarakat."},
            {"name": "Gempa Otomatis", "desc": "Informasi gempa bumi otomatis terbaru."},
        ]
        
        for i, item in enumerate(menu_options):
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

        choice = cyber_input("Pilih informasi yang ingin dilihat")

        if choice in ['0', 'b']:
            break
        
        bmkg_data = get_bmkg_data(config)
        if not bmkg_data:
            cyber_input("Tekan Enter untuk mencoba lagi...")
            continue

        if choice == '1':
            display_gempa_list(bmkg_data.get("gempaterkini", []), "🌍 Gempa Terkini (M > 5.0) 🌍")
        elif choice == '2':
            display_gempa_list(bmkg_data.get("gempadirasakan", []), "🏠 Gempa Dirasakan 🏠")
        elif choice == '3':
            display_autogempa(bmkg_data.get("autogempa", {}))
        else:
            console.print("[bold red]Pilihan tidak valid![/bold red]")
            cyber_input("Tekan Enter untuk melanjutkan...")