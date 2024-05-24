from pystray import Icon, Menu, MenuItem as item
from PIL import Image
import requests
import threading
import os
from io import BytesIO
import webbrowser

# Importing the required functions from other modules
from modules.user_interface import user_confirm
from modules.startup import check_startup, add_to_startup, remove_from_startup
from modules.icon import update_icon_based_on_api
from modules.tools import resource_path


def download_and_save_icon(url, filename):
    response = requests.get(url)
    response.raise_for_status()  # Ensure the request was successful
    image = Image.open(BytesIO(response.content))

    parent_directory = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
    file_path = os.path.join(parent_directory, filename)

    image.save(file_path)
    return file_path


def open_github():
    webbrowser.open("https://github.com/kristiangoystdal/OV_Door/tree/main")


def open_website():
    webbrowser.open("https://omegav.no")


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
    # Update to use the correct path for the icon in the dist directory
    icon_path = os.path.join(os.path.dirname(__file__), "ov_logo.ico")

    # Ensure the icon file is in the correct location
    if not os.path.exists(icon_path):
        icon_path = download_and_save_icon(
            "https://raw.githubusercontent.com/kristiangoystdal/OV_Door/main/ov_logo.ico",
            "ov_logo.ico",
        )

    menu = Menu(
        item("Check out GitHub", open_github),
        item("Open Website", open_website),
        item("Run at Startup", toggle_startup, checked=lambda item: check_startup()),
        item("Quit", quit_program),
    )
    icon_img = Image.open(icon_path)
    icon = Icon("omega_icon", icon_img, "Omega Verksted Door Status", menu)
    threading.Thread(
        target=update_icon_based_on_api, args=(icon, icon_path), daemon=True
    ).start()
    icon.run()
