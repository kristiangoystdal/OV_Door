import pystray
from pystray import MenuItem as item
from PIL import Image, ImageDraw, ImageFont
import requests
import threading
import time
import os
import winreg
import sys


def create_icon_image(color):
    image_size = (128, 128)
    image = Image.new("RGBA", image_size, (255, 255, 255, 0))
    draw = ImageDraw.Draw(image)

    font_path = "C:/Windows/Fonts/arial.ttf"
    max_font_size = 120

    while max_font_size > 10:
        try:
            font = ImageFont.truetype(font_path, max_font_size)
        except IOError:
            font = ImageFont.load_default()

        text = "Ω"
        left, top, right, bottom = font.getbbox(text)
        text_width = right - left
        text_height = bottom - top

        if text_width <= image_size[0] and text_height <= image_size[1]:
            break
        max_font_size -= 2

    text_position = (
        (image_size[0] - text_width) // 2,
        (image_size[1] - text_height) // 2,
    )
    draw.text(text_position, text, font=font, fill=color)

    return image


def format_elapsed_time(seconds):
    hours, remainder = divmod(seconds, 3600)
    minutes, seconds = divmod(remainder, 60)
    return f"{hours}h {minutes}m"


def update_icon_based_on_api(icon):
    while True:
        try:
            response = requests.get("https://omegav.no/api/dooropen.php")
            response.raise_for_status()
            data = response.json()
            is_open = data["open"].strip() == "1"
            elapsed_seconds = int(data["time"])
            color = (0, 255, 0, 255) if is_open else (255, 0, 0, 255)

            elapsed_time = format_elapsed_time(elapsed_seconds)
            print(
                f"Fetched Data: {data}, Is Open: {is_open}, Elapsed Time: {elapsed_time}"
            )

            icon.icon = create_icon_image(color)
            icon.title = f"{'Open' if is_open else 'Closed'} for {elapsed_time}"
        except Exception as e:
            print(f"Error fetching data: {e}")

        time.sleep(60)


def open_website():
    os.system("start https://omegav.no")


def quit_program(icon):
    icon.stop()


def check_startup(*args):
    with winreg.OpenKey(
        winreg.HKEY_CURRENT_USER, "Software\\Microsoft\\Windows\\CurrentVersion\\Run"
    ) as key:
        try:
            winreg.QueryValueEx(key, "MyPythonScript")
            return True
        except FileNotFoundError:
            return False


def add_to_startup(exe_path=None):
    if exe_path is None:
        exe_path = os.path.abspath(sys.argv[0])

    with winreg.OpenKey(
        winreg.HKEY_CURRENT_USER,
        "Software\\Microsoft\\Windows\\CurrentVersion\\Run",
        0,
        winreg.KEY_SET_VALUE,
    ) as key:
        winreg.SetValueEx(key, "MyPythonScript", 0, winreg.REG_SZ, exe_path)
    print("Added to startup")


def remove_from_startup():
    with winreg.OpenKey(
        winreg.HKEY_CURRENT_USER,
        "Software\\Microsoft\\Windows\\CurrentVersion\\Run",
        0,
        winreg.KEY_SET_VALUE,
    ) as key:
        winreg.DeleteValue(key, "MyPythonScript")
    print("Removed from startup")


def toggle_startup(icon, item):
    if check_startup():
        remove_from_startup()
    else:
        add_to_startup()


def create_tray_icon():
    menu = pystray.Menu(
        item("Open Website", open_website),
        item("Run at Startup", toggle_startup, checked=check_startup),
        item("Quit", quit_program),
    )

    icon = pystray.Icon(
        "omega_icon",
        create_icon_image((255, 0, 0, 255)),
        "Omega Verksted Door Status",
        menu,
    )
    threading.Thread(target=update_icon_based_on_api, args=(icon,), daemon=True).start()
    icon.run()


if __name__ == "__main__":
    create_tray_icon()
