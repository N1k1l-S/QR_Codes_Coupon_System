from flask import Flask, render_template, request, jsonify
import os

app = Flask(__name__)

# Dictionary to store used coupon codes
used_coupons = {}

@app.route("/")  
def home():
    return "✅ Flask server is running! Use /validate/<code> to check a QR code."

@app.route("/validate/<code>", methods=["GET", "POST"])
def validate_coupon(code):
    if request.method == "POST":
        if code in used_coupons:
            return jsonify({"status": "error", "message": "Coupon already used!"})
        used_coupons[code] = True
        return jsonify({"status": "success", "message": "Coupon marked as used!"})
    
    # Default GET request (before scanning)
    return f"""
    <h2>Coupon Validation</h2>
    <p>Coupon Code: <strong>{code}</strong></p>
    <form method="POST">
        <button type="submit">Mark as Used</button>
    </form>
    """

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080, debug=True)
