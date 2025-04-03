import qrcode
import pandas as pd
import os
import smtplib
from email.message import EmailMessage

# 🔹 Set your public server URL (after deploying to Railway.app or another service)
PUBLIC_SERVER_URL = "https://N1k1l.pythonanywhere.com"  # Replace with your actual URL

# Ensure QR codes folder exists
QR_CODES_FOLDER = "qrs"
if not os.path.exists(QR_CODES_FOLDER):
    os.makedirs(QR_CODES_FOLDER)

# Read CSV file (modify filename if needed)
csv_filename = "coupons.csv"
df = pd.read_csv(csv_filename)

# Email configuration
EMAIL_SENDER = "YOUR_EMAIL"
EMAIL_PASSWORD = "YOUR_PASSWORD"
# EMAIL_SENDER = "your_email@gmail.com"  # Replace with your email
# EMAIL_PASSWORD = "your_email_password"  # Use an app password if using Gmail
SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 587

# Function to send email with QR code
def send_email(receiver_email, qr_filename, qr_url):
    msg = EmailMessage()
    msg["Subject"] = "Your Event QR Code"
    msg["From"] = EMAIL_SENDER
    msg["To"] = receiver_email
    msg.set_content(f"Scan the QR code or click the link to validate: {qr_url}")

    # Attach QR Code Image
    with open(qr_filename, "rb") as f:
        msg.add_attachment(f.read(), maintype="image", subtype="png", filename=qr_filename)

    # Send email
    with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
        server.starttls()
        server.login(EMAIL_SENDER, EMAIL_PASSWORD)
        server.send_message(msg)

# Generate QR Codes and Send Emails
for index, row in df.iterrows():
    email = row["email"]
    num_coupons = int(row["num_coupons"])

    for i in range(num_coupons):
        coupon_code = f"{email}_{i}"
        qr_url = f"{PUBLIC_SERVER_URL}/validate/{coupon_code}"
        qr_filename = os.path.join(QR_CODES_FOLDER, f"{coupon_code}.png")

        # Generate QR Code
        qr = qrcode.make(qr_url)
        qr.save(qr_filename)

        # Send Email with QR
        send_email(email, qr_filename, qr_url)
        print(f"✅ Sent QR code for {coupon_code} to {email}")

print("🎉 All QR codes generated and sent!")
