import os
import re
import sys
from PIL import Image
import pytesseract
import cv2
from concurrent.futures import ThreadPoolExecutor
import csv

pytesseract.pytesseract.tesseract_cmd = os.path.expandvars(r"%ProgramFiles%\Tesseract-OCR\tesseract.exe")

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
    postcode_regex = r"\b\d{4}\b"
    postcodes = re.findall(postcode_regex, filtered_text)
    return postcodes

def write_to_csv(postcodes, confidences):
    filename = "postcodes.csv"
    rows = zip(postcodes, confidences)
    if os.path.exists(filename):
        existing_postcodes = set()
        with open(filename, "r") as file:
            reader = csv.reader(file)
            for row in reader:
                existing_postcodes.add(row[0])

        rows = filter(lambda row: row[0] not in existing_postcodes, rows)
        if not any(rows):
            return

    with open(filename, "a", newline="") as file:
        writer = csv.writer(file)
        for row in rows:
            writer.writerow(row)

def process_frame(frame):
    text_data = pytesseract.image_to_data(frame)
    filtered_text = filter_output(text_data, 70)
    postcodes = extract_postcode(filtered_text)
    confidences = re.findall(r"conf:(\d+\.\d+)", filtered_text)
    write_to_csv(postcodes, confidences)

def main():
    cam = cv2.VideoCapture("http://192.168.2.149:4747/video/")

    cam.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
    cam.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)

    if not cam.isOpened():
        print("Error opening camera")
        return

    with ThreadPoolExecutor(max_workers=4) as executor:
        while True:
            ret, frame = cam.read()
            if not ret:
                print("Error grabbing the frame")
                break

            executor.submit(process_frame, frame)

            cv2.imshow("Test", frame)

            if cv2.waitKey(1) % 256 == ord("q"):
                print("Quitting...")
                break

    cam.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()