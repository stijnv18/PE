import os
from PIL import Image
import pytesseract
import re
import time as t
from concurrent.futures import ThreadPoolExecutor

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
                filtered_text += line_parts[-1] + " conf:" + conf + "\n"  # Append the last value (text) to filtered_text
    return filtered_text

def extract_postcode(filtered_text):
    postcode_regex = r"\b\d{4}\b"  # Regex pattern for UK postcodes
    postcodes = re.findall(postcode_regex, filtered_text)
    return postcodes

# Specify the path to your image
image_path = "test.png"

# Extract text from the image
def perform_ocr(image_path):
    data = pytesseract.image_to_data(Image.open(image_path))
    return data

start_time = t.time()
num_threads = 800  # Define the number of threads to use

# Create a thread pool executor
with ThreadPoolExecutor(max_workers=num_threads) as executor:
    # Submit the OCR task to the thread pool
    futures = [executor.submit(perform_ocr, image_path) for _ in range(num_threads)]

# Retrieve the results from the completed futures
results = [future.result() for future in futures]
end_time = t.time()
print("Total processing time:", end_time - start_time)

# Filter and extract postcodes from the OCR results
filtered_texts = [filter_output(result, 50) for result in results]
postcodes = []
for filtered_text in filtered_texts:
    postcodes.extend(extract_postcode(filtered_text.split("\n:")[0]))

print(postcodes)