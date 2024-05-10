from pystray import Icon, MenuItem as item
from PIL import Image
import requests
import threading
import os
import pystray
from io import BytesIO

from modules.user_interactions import *
from modules.startup import *
from modules.icon import *


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


def create_tray_icon():
    menu = pystray.Menu(
        item("Open GitHub", open_github),
        item("Open Website", open_website),
        item(
            "Run at Startup",
            lambda icon, item: toggle_startup(icon, item),
            checked=check_startup,
        ),
        item("Quit", quit_program),
    )
    base_icon_url = "https://raw.githubusercontent.com/kristiangoystdal/OV_Door/main/Windows/ov_logo.ico"
    icon_img = Image.open(BytesIO(requests.get(base_icon_url).content))
    icon = Icon("omega_icon", icon_img, "Omega Verksted Door Status", menu)
    threading.Thread(
        target=update_icon_based_on_api, args=(icon, base_icon_url), daemon=True
    ).start()
    icon.run()
