import time
import sys
import pygame
import win32api
import json
from pathlib import Path
import os
from tkinter import Tk, filedialog, simpledialog, messagebox

# Idle threshold in seconds
IDLE_THRESHOLD = 10

# Config file in current directory
CONFIG_FILE = Path(__file__).parent / "config.json"

# --- Function to pick image with GUI ---
def select_image_gui():
    """Open a file dialog to let the user pick an image"""
    root = Tk()
    root.withdraw()  # hide the main window
    root.attributes("-topmost", True)  # bring dialog to front
    file_path = filedialog.askopenfilename(
        title="Select Screensaver Image",
        filetypes=[("Image Files", "*.jpg *.jpeg *.png *.bmp *.gif")]
    )
    root.destroy()
    return file_path

def ask_timeout_gui():
    """Ask user for idle timeout in minutes"""
    root = Tk()
    root.withdraw()
    while True:
        timeout = simpledialog.askstring(
            "Idle Timeout",
            "Enter idle timeout in minutes:"
        )
        if timeout is None:
            messagebox.showerror("Error", "You must enter a timeout value.")
            continue
        try:
            timeout = float(timeout)
            if timeout <= 0:
                raise ValueError
            root.destroy()
            return int(timeout * 60)  # convert minutes to seconds
        except ValueError:
            messagebox.showerror("Error", "Enter a valid positive number.")

# --- Load or create config ---
if CONFIG_FILE.exists():
    with open(CONFIG_FILE, "r") as f:
        config = json.load(f)
    IMAGE_PATH = config.get("image_path", "")
    IDLE_THRESHOLD = int(config.get("timeout", 10))
    if not IMAGE_PATH or not os.path.exists(IMAGE_PATH):
        messagebox.showinfo("Image Path Required", "Please select an image for the screensaver.")
        IMAGE_PATH = select_image_gui()
        IDLE_THRESHOLD = ask_timeout_gui()
        config["image_path"] = IMAGE_PATH
        config["timeout"] = IDLE_THRESHOLD
        with open(CONFIG_FILE, "w") as f:
            json.dump(config, f, indent=4)
else:
    # First time run
    messagebox.showinfo("First Run", "Please select an image for the screensaver.")
    IMAGE_PATH = select_image_gui()
    IDLE_THRESHOLD = ask_timeout_gui()
    config = {"image_path": IMAGE_PATH, "timeout": IDLE_THRESHOLD}
    with open(CONFIG_FILE, "w") as f:
        json.dump(config, f, indent=4)

# Normalize path
IMAGE_PATH = os.path.normpath(IMAGE_PATH)
if not os.path.exists(IMAGE_PATH):
    messagebox.showerror("Error", f"Image not found at {IMAGE_PATH}. Exiting.")
    sys.exit(1)

# --- Functions ---
def get_idle_time():
    """Return idle time in seconds"""
    now = win32api.GetTickCount()
    last_input = win32api.GetLastInputInfo()
    return (now - last_input) / 1000.0

def screensaver():
    """Fullscreen screensaver until key/mouse input"""
    pygame.init()
    screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
    pygame.display.set_caption("Idle Screensaver")

    img = pygame.image.load(IMAGE_PATH)
    img = pygame.transform.scale(img, screen.get_size())

    running = True
    while running:
        for event in pygame.event.get():
            if event.type in (pygame.KEYDOWN, pygame.MOUSEBUTTONDOWN, pygame.QUIT):
                running = False

        screen.blit(img, (0, 0))
        pygame.display.flip()
        pygame.time.delay(30)

    pygame.quit()

# --- Main loop ---
def main():
    while True:
        idle_time = get_idle_time()
        print(f"Idle for {idle_time:.2f} seconds")
        if idle_time >= IDLE_THRESHOLD:
            screensaver()
        time.sleep(1)

if __name__ == "__main__":
    main()
