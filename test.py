import os
from PIL import Image
import pytesseract

pytesseract.pytesseract.tesseract_cmd = os.path.expandvars(r"%ProgramFiles%\Tesseract-OCR\tesseract.exe")

print(pytesseract.image_to_string(Image.open("test.png")))
print("-"*100)
print(pytesseract.image_to_string("test.png"))
print("-"*100)
print(pytesseract.image_to_boxes(Image.open("test.png")))
print("-"*100)
print(pytesseract.image_to_data(Image.open("test.png")))