import os
from PIL import Image
import pytesseract
import re
import time as t
pytesseract.pytesseract.tesseract_cmd = os.path.expandvars(r"%ProgramFiles%\Tesseract-OCR\tesseract.exe")

# Function to filter output based on confidence threshold
def filter_output(text_data, confidence_threshold):
    lines = text_data.split("\n")
    filtered_text = ""
    skip_first_line = True  # Flag to skip the first line
    for line in lines:
        if skip_first_line:
            skip_first_line = False
            continue  # Skip the first line and move to the next iteration
        if line:
            line_parts = line.split("\t")
            conf = line_parts[-2]  # Extract the second-to-last value as confidence
            if float(conf) >= confidence_threshold:
                filtered_text += line_parts[-1]+" conf:"+conf +"\n"  # Append the last value (text) to filtered_text
    return filtered_text

def extract_postcode(filtered_text):
    postcode_regex = r"\b\d{4}\b"  # Regex pattern for UK postcodes
    postcodes = re.findall(postcode_regex, filtered_text)
    return postcodes

# Specify the path to your image
image_path = "test.png"

# Extract text from the image
#text = pytesseract.image_to_string(Image.open(image_path))

# Filter the output based on confidence threshold
startime = t.time()
for i in range(100):
    data = pytesseract.image_to_data(Image.open("test.png"))
stoptime = t.time()
print(stoptime-startime)
filtered_text = filter_output(data, 50)
postcodes = extract_postcode(filtered_text.split("\n:")[0])
print(postcodes)