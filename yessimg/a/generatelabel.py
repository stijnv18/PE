from fpdf import FPDF
from barcode.codex import Code128
from barcode.writer import ImageWriter
import random

def generate_random_address():
    streets = ["Main St", "Oak Ave", "Maple Rd", "Cedar Ln", "Elm St", "Pine Dr", "Birch Ct"]
    # List of common US cities
    cities = ["New York", "Los Angeles", "Chicago", "Houston", "Phoenix", "Philadelphia", "San Antonio",
            "San Diego", "Dallas", "San Jose", "Austin", "Jacksonville", "Fort Worth", "Columbus", "San Francisco"]
    street_number = random.randint(1, 9999)
    street_name = random.choice(streets)
    city = random.choice(cities)
    state = "CA" # You can change this to a random state if desired
    zip_code = random.randint(10000, 99999)
    address = f"{street_number} {street_name} {city}, {state} {zip_code}"
    return address

def generate_labels(scalex=2, scaley=2):
    pdf = FPDF(orientation='P', unit='mm', format='A4')
    sender_name = "John Smith"
    sender_address = "123 Main St \nAnytown, USA 12345"
    tracking_number = "1234567890"
    pdf.set_font('Arial', '', int(10 * scalex))

    for i in range(100):
        pdf.add_page()
        receiver_name = "Jane Doe"
        receiver_address = generate_random_address()
        tracking_number = "1234567890"

        left_margin = 10 * scalex
        top_margin = 10 * scaley
        label_width = 100 * scalex
        label_height = 150 * scaley
        label_padding = 5 * scalex
        barcode_height = 30 * scaley

        pdf.rect(left_margin, top_margin, label_width, label_height)
        pdf.set_font('Arial', 'B', int(24 * scalex))
        pdf.text(left_margin + 7 * scalex, top_margin + 13 * scaley, "P")
        pdf.rect(left_margin + 0, top_margin + 0, 20 * scalex, 20 * scaley)

        pdf.set_font('Arial', '', int(8 * scalex))
        pdf.text(left_margin + 32 * scalex, top_margin + 7 * scaley, "Fees Paid by")

        pdf.rect(left_margin + 0, top_margin + 20 * scaley, label_width, 12 * scaley)
        pdf.set_font('Arial', 'B', int(12 * scalex))
        pdf.text(left_margin + label_width/2, top_margin + 25 * scaley, "Priority Mail")

        ofset = 36 * scaley

        pdf.text(left_margin + 5 * scalex, top_margin + ofset, sender_name)
        pdf.text(left_margin + 5 * scalex, top_margin + ofset+5 * scaley, sender_address)

        pdf.text(left_margin + 5 * scalex, top_margin + 46 * scaley, "SHIP: "+receiver_name)
        pdf.text(left_margin + 5 * scalex, top_margin + 50 * scaley, "TO: "+receiver_address)
        code128 = Code128(tracking_number, writer=ImageWriter())
        barcode_file = code128.save('barcode')
        pdf.image(barcode_file, left_margin + 5 * scalex, top_margin + 50 * scaley, w=label_width - label_padding-20 * scalex, h=barcode_height)

    pdf_file = "labels.pdf"
    pdf.output(pdf_file, 'F')
    print("Labels generated: " + pdf_file)

generate_labels(scalex=1.5,scaley=1.5)