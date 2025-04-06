import csv
from flask import Flask, render_template, request
import os

app = Flask(__name__)

# Password to validate
VALIDATION_PASSWORD = "tca25"

# File to save used coupon data
USED_COUPONS_FILE = "used_coupons.csv"

# Load already used coupons (if file exists)
used_coupons = {}
if os.path.exists(USED_COUPONS_FILE):
    with open(USED_COUPONS_FILE, "r") as f:
        reader = csv.reader(f)
        for row in reader:
            code = row[0]
            used_coupons[code] = True

@app.route("/")
def home():
    return "✅ QR Code Validation Server Running! Use /validate/<code>"

@app.route("/validate/<code>", methods=["GET", "POST"])
def validate_coupon(code):
    error = None
    success = None

    if request.method == "POST":
        password = request.form.get("password")

        if password != VALIDATION_PASSWORD:
            error = "❌ Incorrect Password!"
        elif code in used_coupons:
            error = "❌ Coupon already used!"
        else:
            used_coupons[code] = True
            # Save to file
            with open(USED_COUPONS_FILE, "a", newline='') as f:
                writer = csv.writer(f)
                writer.writerow([code])
            success = "✅ Coupon successfully validated!"

    return render_template("validate.html", code=code, used=code in used_coupons, error=error, success=success)

@app.route("/used-coupons")
def show_used():
    return f"<h2>Used Coupons</h2><ul>{''.join(f'<li>{c}</li>' for c in used_coupons)}</ul>"

if __name__ == "__main__":
    app.run()
