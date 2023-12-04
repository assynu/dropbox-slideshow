from PIL import Image, ImageTk
import tkinter as tk
import modules.console as console
from time import sleep, time

paths = [
    "images/land_1.jpg",
    "images/land_2.jpg",
    "images/land_1.jpg",
    "images/land_3.jpg",
    "images/land_2.jpg",
    "images/land_1.jpg",
]

transition_duration = 5  # in seconds

def load_image(path, screen_width, screen_height):
    try:
        image = Image.open(path).resize((screen_width, screen_height))
        tk_image = ImageTk.PhotoImage(image)
        return tk_image
    except Exception as e:
        console.error(f"Error loading image {path}: {e}")
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

def main():
    console.clear()
    root = tk.Tk()
    root.attributes('-fullscreen', True)

    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()

    console.log("Starting image transitions...")

    canvas = tk.Canvas(root, width=screen_width, height=screen_height)
    canvas.pack(fill=tk.BOTH, expand=True)

    photo_images = []

    for i in range(len(paths)):
        current_path = paths[i]
        next_path = paths[(i + 1) % len(paths)]  # Wrap around for the last image

        console.log(f"Attempting to transition from {current_path} to {next_path}...")

        tk_current_image = load_image(current_path, screen_width, screen_height)
        tk_next_image = load_image(next_path, screen_width, screen_height)

        if tk_current_image is None or tk_next_image is None:
            console.error("Failed to load images. Skipping transition.")
            continue

        photo_images.extend([tk_current_image, tk_next_image])

        display_image(canvas, tk_current_image)
        root.update_idletasks()
        root.update()

        sleep(1)  # Add a delay before starting the transition

        transition_images(root, canvas, tk_current_image, tk_next_image)

        console.success(f"Transition from {current_path} to {next_path} complete.")
        sleep(5)  # Display each image for 5 seconds

    console.log("All image transitions completed.")

    # Clean up PhotoImage references
    for img in photo_images:
        img.__del__()

    root.destroy()

if __name__ == '__main__':
    main()
