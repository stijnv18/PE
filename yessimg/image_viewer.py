import os
import shutil
import tkinter as tk
from tkinter import filedialog
from PIL import ImageTk, Image

# Set up the main window
root = tk.Tk()
root.geometry("500x500")
root.title("Image Viewer")

# Ask user to select folder containing images
folder_path = filedialog.askdirectory(title="Select folder containing images")

# Get a list of all image files in the folder
image_extensions = [".jpg", ".jpeg", ".png", ".gif"]
image_files = [f for f in os.listdir(folder_path) if f.endswith(tuple(image_extensions))]

# Create a new folder to save copied images
new_folder_path = os.path.join(folder_path, "copied_images")
os.makedirs(new_folder_path, exist_ok=True)
def on_key_press(event):
    print("test")
    if event.keysym == 'y':
        copy_image()
    elif event.keysym == 'n':
        show_next_image()
# Function to copy the image to the new folder
def copy_image(event):
    print("boo")
    shutil.copyfile(os.path.join(folder_path, image_files[image_index]), os.path.join(new_folder_path, image_files[image_index]))
    show_next_image('a')
    

# Function to display the next image
def show_next_image(event):
    print("test")
    global image_index, image_label, yes_button, no_button
    image_index += 1
    if image_index >= len(image_files):
        image_label.configure(text="End of images.")
        yes_button.configure(state="disabled")
        no_button.configure(state="disabled")
    else:
        # Load the image and scale it to fit the window while maintaining its aspect ratio
        image_path = os.path.join(folder_path, image_files[image_index])
        image = Image.open(image_path)
        w, h = root.winfo_width(), root.winfo_height() - 100
        image.thumbnail((w, h), Image.ANTIALIAS)
        photo_image = ImageTk.PhotoImage(image)
        
        # Update the image label with the new image
        image_label.configure(image=photo_image)
        image_label.image = photo_image
        yes_button.configure(state="normal")
        no_button.configure(state="normal")

# Display the first image
image_index = 0
image_path = os.path.join(folder_path, image_files[image_index])
image = Image.open(image_path)
w, h = root.winfo_width(), root.winfo_height() - 100
image.thumbnail((w, h), Image.ANTIALIAS)
photo_image = ImageTk.PhotoImage(image)
image_label = tk.Label(root, image=photo_image)
image_label.pack(pady=20)

# Add "Yes" and "No" buttons
yes_button = tk.Button(root, text="Yes", command=copy_image)
yes_button.pack(side=tk.LEFT, padx=50)
no_button = tk.Button(root, text="No", command=show_next_image)
no_button.pack(side=tk.RIGHT, padx=50)

# Bind keyboard shortcuts to "Yes" and "No" buttons
root.bind('<Return>', copy_image)
root.bind('<n>', show_next_image)
# Start the main loopnnn
root.focus_force()
root.mainloop()