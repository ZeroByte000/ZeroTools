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
from app.console import console, print_cyber_panel, cyber_input, create_menu_table, clear

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
        print_cyber_panel("AI Tools Menu", "Pilih alat AI yang ingin digunakan")

        ai_options = [
            "Image to Anime",
            "Penghitam Waifu",
            "Mistral Ai",
            "ChatGPT Ai",
            "ChatGPT V2",
            "Deepseek Ai",
            "Gemini Ai",
            "Colorize Ai",
            "Waifu2x",
            "TxT to Image",
            "TxT to Image (v2)",
            "Flux Schnell",
        ]
        
        menu_table = create_menu_table("[bold blue]AI Sub-Menu[/bold blue]", ai_options)
        console.print(menu_table)

        choice = cyber_input("Pilih alat AI")

        if choice in menu_actions:
            menu_actions[choice]()
        elif choice in ['0', 'b']:
            break
        else:
            console.print("[bold red]Pilihan tidak valid![/bold red]")
            cyber_input("Tekan Enter untuk melanjutkan...")