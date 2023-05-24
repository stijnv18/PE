import os
import re
import sys
from PIL import Image # pip install Pillow
import pytesseract # pip install pytesseract
import cv2 # pip install opencv-python

pytesseract.pytesseract.tesseract_cmd = os.path.expandvars(r"%ProgramFiles%\Tesseract-OCR\tesseract.exe")

def main():
	cam = cv2.VideoCapture(0, cv2.CAP_DSHOW) # Try cv2.CAP_AVFOUNDATION if error

	cam.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
	cam.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)

	if not cam.isOpened():
		print("Error opening camera")
		return

	while True:
		ret, frame = cam.read()
		if not ret:
			print("Error grabbing the frame")
			break
		
		
		print(pytesseract.image_to_string(frame))
		"""
		print(pytesseract.image_to_string(Image.open(img)))
		print("-"*100)
		print(pytesseract.image_to_string(img))
		print("-"*100)
		print(pytesseract.image_to_boxes(Image.open(img)))
		print("-"*100)
		print(pytesseract.image_to_data(Image.open(img)))
		print("*"*100)
		"""

		cv2.imshow("Test", frame)

		if cv2.waitKey(1) % 256 == ord("q"):
			print("Quitting...")
			break

	cam.release()
	cv2.destroyAllWindows()

if __name__ == "__main__":
	main()