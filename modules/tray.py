from pystray import Icon, Menu, MenuItem as item
from PIL import Image
import requests
import threading
import os
from io import BytesIO

# Assuming these imports are correct and available
from modules.user_interface import user_confirm
from modules.startup import check_startup, add_to_startup, remove_from_startup
from modules.icon import update_icon_based_on_api
from modules.updates import start_gui  # Assuming start_gui is in modules.updates


def open_github():
    os.system("start https://github.com/kristiangoystdal/OV_Door/tree/main")


def open_website():
    os.system("start https://omegav.no")


def quit_program(icon):
    icon.stop()


def toggle_startup(icon, item):
    startup_enabled = check_startup()
    if startup_enabled and user_confirm("Do you want to remove this app from startup?"):
        remove_from_startup()
    elif not startup_enabled and user_confirm(
        "Do you want to add this app to startup?"
    ):
        add_to_startup()


def run_updater(icon, item):
    threading.Thread(target=start_gui, daemon=True).start()


def create_tray_icon():
    menu = Menu(
        item("Omega Verksted Door Status", open_github),
        item("Check for Updates", run_updater),
        item("Check out GitHub", open_github),
        item("Open Website", open_website),
        item("Run at Startup", toggle_startup, checked=lambda item: check_startup()),
        item("Quit", quit_program),
    )
    base_icon_url = (
        "https://raw.githubusercontent.com/kristiangoystdal/OV_Door/main/ov_logo.ico"
    )
    icon_img = Image.open(BytesIO(requests.get(base_icon_url).content))
    icon = Icon("omega_icon", icon_img, "Omega Verksted Door Status", menu)
    threading.Thread(
        target=update_icon_based_on_api, args=(icon, base_icon_url), daemon=True
    ).start()
    icon.run()


if __name__ == "__main__":
    create_tray_icon()
