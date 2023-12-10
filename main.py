import os
import random
from threading import Thread
from PIL import Image, ImageTk
import tkinter as tk
import dropbox
from time import sleep, time
from pynput.keyboard import Key, Listener
import cv2

from modules.console import error, log, success, clear
from modules.console.formats import TEXT_FORMATS

TRANSITION_COOLDOWN = 2
TRANSITION_DURATION = 2
DROPBOX_TOKEN = "sl.Brd9iG-BZTwjDeX6Hv9fXFoq0oDQdNn6irN7MjjCU4yuzZBunlcHbAzN8u2Lpiwy69sJIT_tCkR6fF2pEscljBBklSwp9Q0cylDrYt_Z7NRdGF_OWk86HmnhWy3pmWYBhP_vVc3dEhbAxAMa6XZf"

dbx = dropbox.Dropbox(DROPBOX_TOKEN)
dbx.users_get_current_account()

def load_media(path, screen_width, screen_height):
    _, ext = os.path.splitext(path.lower())
    try:
        if ext in {'.jpg', '.jpeg', '.png', '.gif'}:
            image = Image.open(path).resize((screen_width, screen_height))
            tk_media = ImageTk.PhotoImage(image)
            return tk_media
        elif ext in {'.mp4', '.avi', '.mkv'}:
            cap = cv2.VideoCapture(path)
            ret, frame = cap.read()
            if ret:
                frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                image = Image.fromarray(frame).resize((screen_width, screen_height))
                tk_media = ImageTk.PhotoImage(image)
                cap.release()
                return tk_media
            else:
                error(f"Failed to load video frame from {path}")
                return None
        else:
            error(f"Unsupported file format: {ext}")
            return None
    except Exception as e:
        error(f"Loading media {path}: {e}")
        return None

def display_media(canvas, media):
    canvas.create_image(0, 0, anchor=tk.NW, image=media)

def blend_media(tk_current_media, tk_next_media, alpha):
    blended_media = Image.blend(
        ImageTk.getimage(tk_current_media),
        ImageTk.getimage(tk_next_media),
        alpha
    )
    return ImageTk.PhotoImage(blended_media)

def transition_media(root, canvas, tk_current_media, tk_next_media):
    start_time = time()
    elapsed_time = 0

    while elapsed_time < TRANSITION_DURATION:
        alpha = min(1.0, elapsed_time / TRANSITION_DURATION)
        tk_blended_media = blend_media(tk_current_media, tk_next_media, alpha)
        display_media(canvas, tk_blended_media)
        root.update_idletasks()
        root.update()

        elapsed_time = time() - start_time

    display_media(canvas, tk_next_media)
    root.update_idletasks()
    root.update()

def get_random_media(entries, current_path=None):
    if len(entries) > 0:
        random_index = random.randint(0, len(entries) - 1)
        entry = entries[random_index]

        if isinstance(entry, dropbox.files.FileMetadata):
            if current_path is not None and entry.path_lower == current_path:
                entry = entries[random.randint(0, len(entries) - 1)]

            log(f"{TEXT_FORMATS.OKCYAN}Downloading{TEXT_FORMATS.ENDC} {TEXT_FORMATS.UNDERLINE}{entry.name}{TEXT_FORMATS.ENDC}...")

            path = f"Media/{entry.name}"
            dbx.files_download_to_file(path, entry.path_lower)

            success(f"{TEXT_FORMATS.OKBLUE}Downloaded{TEXT_FORMATS.ENDC} {TEXT_FORMATS.UNDERLINE}{entry.name}{TEXT_FORMATS.ENDC} to {TEXT_FORMATS.UNDERLINE}{path}{TEXT_FORMATS.ENDC}.")

            return path

def display_media_files(_):
    root = tk.Tk()
    root.attributes('-fullscreen', True)

    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()

    log("Starting media transitions...")

    canvas = tk.Canvas(root, width=screen_width, height=screen_height)
    canvas.pack(fill=tk.BOTH, expand=True)

    last_media = None

    while True:
        entries = get_dropbox_media()

        if last_media is None:
            last_media = get_random_media(entries)

        current_path = last_media
        next_path = get_random_media(entries, last_media)

        last_media = next_path

        log(f"Attempting to transition from {TEXT_FORMATS.UNDERLINE}{current_path}{TEXT_FORMATS.ENDC} to {TEXT_FORMATS.UNDERLINE}{next_path}{TEXT_FORMATS.ENDC}...")

        tk_current_media = load_media(current_path, screen_width, screen_height)
        tk_next_media = load_media(next_path, screen_width, screen_height)

        if tk_current_media is None or tk_next_media is None:
            error("Failed to load media. Skipping transition.")
            continue

        display_media(canvas, tk_current_media)
        root.update_idletasks()
        root.update()

        sleep(1)

        transition_media(root, canvas, tk_current_media, tk_next_media)

        success(f"Transition from {TEXT_FORMATS.UNDERLINE}{current_path}{TEXT_FORMATS.ENDC} to {TEXT_FORMATS.UNDERLINE}{next_path}{TEXT_FORMATS.ENDC} complete.")

        if os.path.isfile(current_path):
            os.remove(current_path)
            success(f"{TEXT_FORMATS.FAIL}Deleted {TEXT_FORMATS.ENDC}{TEXT_FORMATS.UNDERLINE}{current_path}{TEXT_FORMATS.ENDC}.")
        else:
            error("%s file not found" % current_path)

        sleep(TRANSITION_COOLDOWN)

def get_dropbox_media():
    return dbx.files_list_folder('/Slideshow').entries

def keyboard_listener(_):
    def on_release(key):
        if key == Key.esc:
            log("Exiting...")
            os._exit(0)

    while True:
        print(1)
        with Listener(on_release=on_release) as listener:
            listener.join()

def main():
    clear()

    thread_1 = Thread(target=keyboard_listener, args=(10,))
    thread_1.start()

    thread_2 = Thread(target=display_media_files, args=(10,))
    thread_2.start()

    thread_1.join()
    thread_2.join()

if __name__ == '__main__':
    main()
