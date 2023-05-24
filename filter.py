import os
from PIL import Image
import pytesseract

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


# Specify the path to your image
image_path = "test.png"

# Extract text from the image
text = pytesseract.image_to_string(Image.open(image_path))

# Filter the output based on confidence threshold
data = pytesseract.image_to_data(Image.open("test.png"))
filtered_text = filter_output(data, 50)

print(filtered_text)