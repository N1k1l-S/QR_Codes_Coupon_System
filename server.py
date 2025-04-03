from flask import Flask, render_template, request, jsonify
import os

app = Flask(__name__)

# Dictionary to store used coupon codes
used_coupons = {}

# Set a password for validation
VALIDATION_PASSWORD = "tca"

@app.route("/")
def home():
    return "✅ QR Code Validation Server is Running! Use /validate/<code> to check a QR code."

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
            success = "✅ Coupon successfully validated!"

    return render_template("validate.html", code=code, used=code in used_coupons, error=error, success=success)

if __name__ == "__main__":
    app.run()
