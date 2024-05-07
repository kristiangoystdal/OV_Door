from pystray import Icon, MenuItem as item
from PIL import Image
import requests
import threading
import time
import os
import winreg
import sys
import pystray
from io import BytesIO
from datetime import datetime


def change_hue(image, target_hue):
    hsv_image = image.convert("HSV")
    h, s, v = hsv_image.split()
    alpha = image.getchannel("A")

    new_h = Image.new("L", h.size, target_hue)

    hsv_shifted = Image.merge("HSV", (new_h, s, v))
    rgb_shifted = hsv_shifted.convert("RGBA")
    rgb_shifted.putalpha(alpha)  # Restore original alpha
    return rgb_shifted


def format_elapsed_time(seconds):
    hours, remainder = divmod(seconds, 3600)
    minutes, seconds = divmod(remainder, 60)
    return f"{hours}h {minutes}m"


def update_icon_based_on_api(icon, base_icon_path):
    base_icon = Image.open(BytesIO(requests.get(base_icon_path).content)).convert(
        "RGBA"
    )
    last_status = None

    while True:
        try:
            response = requests.get("https://omegav.no/api/dooropen.php")
            response.raise_for_status()
            data = response.json()
            is_open = data.get("open") == "1"
            elapsed_seconds = int(data.get("time", 0))

            elapsed_time = format_elapsed_time(elapsed_seconds)
            print(
                f"Fetched Data: {data}, Is Open: {is_open}, Elapsed Time: {elapsed_time}"
            )

            target_hue = 85 if is_open else 0  # Approximate hue value for green and red
            hue_shifted_icon = change_hue(base_icon, target_hue)

            icon.icon = hue_shifted_icon
            icon.title = f"{'Open' if is_open else 'Closed'} for {elapsed_time}"

            last_status = is_open

        except requests.RequestException as e:
            print(f"Error fetching data: {e}")

        except Exception as e:
            print(f"An error occurred: {e}")

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

    base_icon_url = "https://raw.githubusercontent.com/kristiangoystdal/OV_Door/main/Windows/ov_logo.ico"

    icon_img = Image.open(BytesIO(requests.get(base_icon_url).content))
    icon = Icon(
        "omega_icon",
        icon_img,
        "Omega Verksted Door Status",
        menu,
    )
    threading.Thread(
        target=update_icon_based_on_api, args=(icon, base_icon_url), daemon=True
    ).start()
    icon.run()


if __name__ == "__main__":
    create_tray_icon()
