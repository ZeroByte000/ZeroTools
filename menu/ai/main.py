# menu/ai/main.py

from .functions.image_to_anime import image_to_anime
from .functions.penghitam_waifu import penghitam_waifu
from .functions.mistral_ai import mistral_ai
from .functions.chatgpt_ai import chatgpt_ai
from .functions.chatgpt_v2 import chatgpt_v2
from .functions.deepseek_ai import deepseek_ai
from .functions.gemini_ai import gemini_ai
from .functions.colorize_ai import colorize_ai
from .functions.waifu2x import waifu2x
from .functions.txt_to_image import txt_to_image
from .functions.txt_to_image_v2 import txt_to_image_v2
from .functions.flux_schnell import flux_schnell
from app.console import console, cyber_input, clear
from rich.table import Table
from rich.panel import Panel
from rich.box import SQUARE


def main():
    """Fungsi utama untuk menu AI. Ini yang dipanggil oleh main.py."""
    menu_actions = {
        '1': image_to_anime,
        '2': penghitam_waifu,
        '3': mistral_ai,
        '4': chatgpt_ai,
        '5': chatgpt_v2,
        '6': deepseek_ai,
        '7': gemini_ai,
        '8': colorize_ai,
        '9': waifu2x,
        '10': txt_to_image,
        '11': txt_to_image_v2,
        '12': flux_schnell,
    }

    while True:
        clear()

        table = Table(
            show_header=True,
            header_style="bold #00F0FF",
            title="[bold magenta]✨ AI Tools ✨[/bold magenta]",
            title_style="bold magenta",
            title_justify="center",
            box=SQUARE,
            border_style="#00F0FF", 
            show_lines=True,
            expand=True,
            padding=(0, 1)
        )

        table.add_column("No.", style="bold white", width=4, justify="center")
        table.add_column("Menu", style="bold white", overflow=None)
        table.add_column("Deskripsi", style="bold white", overflow=None)

        ai_options = [
            {"name": "Image to Anime", "desc": "Ubah gambar jadi anime."},
            {"name": "Penghitam Waifu", "desc": "Terapkan filter gelap."},
            {"name": "Mistral Ai", "desc": "Chatbot AI percakapan."},
            {"name": "ChatGPT Ai", "desc": "Chatbot AI populer."},
            {"name": "ChatGPT V2", "desc": "ChatGPT dengan analisis gambar."},
            {"name": "Deepseek Ai", "desc": "Chatbot AI alternatif."},
            {"name": "Gemini Ai", "desc": "AI dari Google dengan analisis gambar."},
            {"name": "Colorize Ai", "desc": "Warnai gambar hitam-putih."},
            {"name": "Waifu2x", "desc": "Tingkatkan kualitas gambar anime."},
            {"name": "TxT to Image", "desc": "Buat gambar dari teks."},
            {"name": "TxT to Image (v2)", "desc": "Pembuat gambar versi 2."},
            {"name": "Flux Schnell", "desc": "Buat gambar dari teks (cepat)."},
        ]
        
        for i, item in enumerate(ai_options):
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

        choice = cyber_input("Pilih alat AI")

        if choice in menu_actions:
            menu_actions[choice]()
        elif choice in ['0', 'b']:
            break
        else:
            console.print("[bold red]Pilihan tidak valid![/bold red]")
            cyber_input("Tekan Enter untuk melanjutkan...")