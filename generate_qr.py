import csv
import qrcode
import smtplib
import socket
import os
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders

# Set this to your PythonAnywhere domain
PUBLIC_SERVER_URL = "https://N1k1l.pythonanywhere.com"

# Email configuration (use your own email and app password)
SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 587
EMAIL_ADDRESS = "YOUR_EMAIL"
EMAIL_PASSWORD = "YOUR_PASSWORD"

# Ensure QR codes directory exists
QR_CODES_FOLDER = "qrs"
if not os.path.exists(QR_CODES_FOLDER):
    os.makedirs(QR_CODES_FOLDER)

# Read CSV and generate QR codes
def generate_qr_codes(csv_filename):
    with open(csv_filename, newline='') as csvfile:
        reader = csv.reader(csvfile)
        next(reader)  # Skip header row

        for row in reader:
            email, num_coupons = row[0], int(row[1])

            for i in range(num_coupons):
                coupon_code = f"{email}_{i}"
                qr_url = f"{PUBLIC_SERVER_URL}/validate/{coupon_code}"
                
                # Generate QR Code
                qr = qrcode.make(qr_url)
                qr_path = f"{QR_CODES_FOLDER}/{coupon_code}.png"
                qr.save(qr_path)

                # Send email with QR code
                send_email(email, qr_path, qr_url)

def send_email(recipient_email, qr_path, qr_url):
    msg = MIMEMultipart()
    msg["From"] = EMAIL_ADDRESS
    msg["To"] = recipient_email
    msg["Subject"] = "Your Event QR Code"

    body = f"Scan this QR code to validate your coupon: {qr_url}"
    msg.attach(MIMEText(body, "plain"))

    with open(qr_path, "rb") as attachment:
        part = MIMEBase("application", "octet-stream")
        part.set_payload(attachment.read())
        encoders.encode_base64(part)
        part.add_header("Content-Disposition", f"attachment; filename={os.path.basename(qr_path)}")
        msg.attach(part)

    with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
        server.starttls()
        server.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
        server.sendmail(EMAIL_ADDRESS, recipient_email, msg.as_string())

    print(f"Sent QR code to {recipient_email}")

# Run the QR generation
generate_qr_codes("coupons.csv")
