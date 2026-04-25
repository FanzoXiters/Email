from flask import Flask, request, jsonify
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import os

app = Flask(__name__)

# ambil dari environment (WAJIB di set di Railway)
SEND_EMAIL = os.environ.get("EMAIL_USER")
SEND_PASSWORD = os.environ.get("EMAIL_PASS")

@app.route("/")
def home():
    return "API aktif!"

@app.route("/send", methods=["POST"])
def send():
    try:
        # 🔐 cek ENV dulu
        if not SEND_EMAIL or not SEND_PASSWORD:
            return jsonify({"status": False, "error": "ENV belum diset"}), 500

        data = request.get_json()

        # ❌ kalau body kosong
        if not data:
            return jsonify({"status": False, "error": "Body JSON kosong"}), 400

        # ambil data aman
        name = data.get("name")
        email = data.get("email")
        subject = data.get("subject")
        body = data.get("body")

        # ❌ kalau ada yang kosong
        if not all([name, email, subject, body]):
            return jsonify({"status": False, "error": "Data tidak lengkap"}), 400

        # ✉️ buat email
        message = MIMEMultipart()
        message["From"] = f"{name} <{SEND_EMAIL}>"
        message["To"] = email
        message["Subject"] = subject

        message.attach(MIMEText(body, "html"))

        # 🚀 kirim email
        with smtplib.SMTP("smtp.gmail.com", 587) as server:
            server.starttls()
            server.login(SEND_EMAIL, SEND_PASSWORD)
            server.sendmail(SEND_EMAIL, email, message.as_string())

        return jsonify({"status": True, "msg": "Email terkirim"})

    except Exception as e:
        return jsonify({"status": False, "error": str(e)}), 500


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)000)
