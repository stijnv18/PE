import cv2
import math
import pytesseract
import os
pytesseract.pytesseract.tesseract_cmd = os.path.expandvars(r"%ProgramFiles%\Tesseract-OCR\tesseract.exe")
def rotate_image(image_path):
    # Load the image
    image = cv2.imread(image_path)

    # Convert the image to grayscale
    #gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # Apply text orientation detection using pytesseract
    orientation = pytesseract.image_to_osd('test.jpg')
    angle = int(orientation.split("\n")[2].split(":")[1])

    # Rotate the image to straighten it
    rotated_image = cv2.rotate(image, cv2.ROTATE_90_CLOCKWISE)

    # Save the rotated image
    output_path = "rotated_image.png"
    cv2.imwrite(output_path, rotated_image)

    return output_path, angle

# Specify the path to your image
image_path = "test.jpg"

# Rotate the image and save the rotated image
rotated_image, angle = rotate_image(image_path)

print("Rotated image saved as:", rotated_image)
print("Calculated angle:", angle)
