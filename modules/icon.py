from PIL import Image
import requests
import time
from io import BytesIO
import os


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
    try:
        if not os.path.isfile(base_icon_path):
            raise FileNotFoundError(f"Icon file not found: {base_icon_path}")

        base_icon = Image.open(base_icon_path).convert("RGBA")
    except Exception as e:
        print(f"An error occurred while opening the base icon: {e}")
        return

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

        except requests.RequestException as e:
            print(f"Error fetching data: {e}")
        except Exception as e:
            print(f"An error occurred: {e}")

        time.sleep(60)
