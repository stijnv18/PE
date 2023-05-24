import os
import random
from PIL import Image
# path to the folder containing images
folder_path = "./b"
# iterate through all files in the folder
for file_name in os.listdir(folder_path):
    if file_name.endswith(".jpg") or file_name.endswith(".png"):
        # open the image file
        img_path = os.path.join(folder_path, file_name)
        img = Image.open(img_path)

        # generate a random angle between -180 and 180 degrees
        angle = random.randint(-180, 180)

        # rotate the image by the random angle
        rotated_img = img.rotate(angle)

        # save the rotated image
        rotated_img.save(img_path)