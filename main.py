import os
import re
import sys
from PIL import Image
import pytesseract
import cv2
from concurrent.futures import ThreadPoolExecutor

pytesseract.pytesseract.tesseract_cmd = os.path.expandvars(r"%ProgramFiles%\Tesseract-OCR\tesseract.exe")

def process_frame(frame):
    text = pytesseract.image_to_string(frame)
    print(text)

def main():
    cam = cv2.VideoCapture("http://192.168.2.149:4747/video/")

    cam.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
    cam.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)

    if not cam.isOpened():
        print("Error opening camera")
        return

    with ThreadPoolExecutor(max_workers=64) as executor:
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