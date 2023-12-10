import os
import random
from threading import Thread
from PIL import Image, ImageTk
import tkinter as tk
import modules.console as console
import dropbox
from time import sleep, time
from modules.console.formats import TEXT_FORMATS
from pynput.keyboard import Key, Listener


transition_cooldown = 2  # for what time image will appear on screen in seconds
transition_duration = 2  # how long will duration take in seconds
dropbox_token = "sl.BrP7zigSI2Rd49V85uDiIj5Gqby8UBhs2bZtD5pyctN5Kjjd8vWkDjMUdLq28WrjR81hoX7F2YiidolvqjbWRlT1Hi6iaq7Z5UYqqxYTj_nsv-PiQWlc4ACp4jlqRfHlWnfQeRYMecoIsWs_98Mb"

dbx = dropbox.Dropbox(dropbox_token)
dbx.users_get_current_account()

def load_image(path, screen_width, screen_height):
    try:
        image = Image.open(path).resize((screen_width, screen_height))
        tk_image = ImageTk.PhotoImage(image)
        return tk_image
    except Exception as e:
        console.error(f"Loading image {path}: {e}")
        return None

def display_image(canvas, image):
    canvas.create_image(0, 0, anchor=tk.NW, image=image)

def blend_images(tk_current_image, tk_next_image, alpha):
    blended_image = Image.blend(
        ImageTk.getimage(tk_current_image),
        ImageTk.getimage(tk_next_image),
        alpha
    )
    return ImageTk.PhotoImage(blended_image)

def transition_images(root, canvas, tk_current_image, tk_next_image):
    start_time = time()
    elapsed_time = 0


    while elapsed_time < transition_duration:
        alpha = min(1.0, elapsed_time / transition_duration)
        tk_blended_image = blend_images(tk_current_image, tk_next_image, alpha)
        display_image(canvas, tk_blended_image)
        root.update_idletasks()
        root.update()

        elapsed_time = time() - start_time

    display_image(canvas, tk_next_image)
    root.update_idletasks()
    root.update()

def get_random_image(entries, current_path=None):
    if len(entries) > 0:
        radnomIndex = random.randint(0, len(entries) - 1)

        entry = entries[radnomIndex]

        if isinstance(entry, dropbox.files.FileMetadata):
            if current_path is not None and entry.path_lower == current_path:
                entry = entries[random.randint(0, len(entries) - 1)]

            console.log(f"{TEXT_FORMATS.OKCYAN}Downloading{TEXT_FORMATS.ENDC} {TEXT_FORMATS.UNDERLINE}{entry.name}{TEXT_FORMATS.ENDC}...")

            path = f"Images/{entry.name}"
            dbx.files_download_to_file(path, entry.path_lower)

            console.success(f"{TEXT_FORMATS.OKBLUE}Downloaded{TEXT_FORMATS.ENDC} {TEXT_FORMATS.UNDERLINE}{entry.name}{TEXT_FORMATS.ENDC} to {TEXT_FORMATS.UNDERLINE}{path}{TEXT_FORMATS.ENDC}.")

            return path

def display_images(_):
    root = tk.Tk()
    root.attributes('-fullscreen', True)

    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()

    console.log("Starting image transitions...")

    canvas = tk.Canvas(root, width=screen_width, height=screen_height)
    canvas.pack(fill=tk.BOTH, expand=True)

    photo_images = []

    lastimage = None

    while True:
        entries = get_dropbox_images()

        if lastimage is None:
            lastimage = get_random_image(entries)

        current_path = lastimage
        next_path = get_random_image(entries, lastimage)

        lastimage = next_path

        console.log(f"Attempting to transition from {TEXT_FORMATS.UNDERLINE}{current_path}{TEXT_FORMATS.ENDC} to {TEXT_FORMATS.UNDERLINE}{next_path}{TEXT_FORMATS.ENDC}...")

        tk_current_image = load_image(current_path, screen_width, screen_height)
        tk_next_image = load_image(next_path, screen_width, screen_height)

        if tk_current_image is None or tk_next_image is None:
            console.error("Failed to load images. Skipping transition.")
            continue

        photo_images.extend([tk_current_image, tk_next_image])

        display_image(canvas, tk_current_image)
        root.update_idletasks()
        root.update()

        sleep(1)

        transition_images(root, canvas, tk_current_image, tk_next_image)

        console.success(f"Transition from {TEXT_FORMATS.UNDERLINE}{current_path}{TEXT_FORMATS.ENDC} to {TEXT_FORMATS.UNDERLINE}{next_path}{TEXT_FORMATS.ENDC} complete.")

        if os.path.isfile(current_path):
            os.remove(current_path)
            console.success(f"{TEXT_FORMATS.FAIL}Deleted {TEXT_FORMATS.ENDC}{TEXT_FORMATS.UNDERLINE}{current_path}{TEXT_FORMATS.ENDC}.")
        else:
            console.error("%s file not found" % current_path)

        sleep(transition_cooldown)

def get_dropbox_images():
    return dbx.files_list_folder('/Slideshow').entries

def keyboard_listener(_):
    def on_release(key):
        if key == Key.esc:
            console.log("Exiting...")
            sleep(3)

            os._exit(0)

    
    while True:
        print(1)
        with Listener(on_release=on_release) as listener:
            listener.join()

def main():
    console.clear()

    thread_1 = Thread(target = keyboard_listener, args = (10, ))
    thread_1.start()

    thread_2 = Thread(target = display_images, args = (10, ))
    thread_2.start()
    
    thread_1.join()
    thread_2.join()
    # display_images()

if __name__ == '__main__':
    main()
