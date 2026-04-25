from flask import Flask, request, jsonify
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import os
from dotenv import load_dotenv


app = Flask(__name__)

# Gunakan App Password 16 digit di sini

load_dotenv()
SEND_EMAIL = os.getenv("EMAIL_USER")
SEND_PASSWORD = os.getenv("EMAIL_PASS")

@app.route("/")
def home():
    return "API aktif!"

@app.route("/send", methods=["POST"])
def send():
    try:
        data = request.get_json()
        if not data:
            return jsonify({"error": "Content-Type harus application/json"}), 400

        name = data.get("name")
        email = data.get("email")
        subject = data.get("subject")
        body = data.get("body")

        if not all([name, email, subject, body]):
            return jsonify({"error": "Data tidak lengkap"}), 400

        # Setting Email
        message = MIMEMultipart()
        message["From"] = SEND_EMAIL
        message["To"] = email
        message["Subject"] = subject
        message.attach(MIMEText(body, "html"))

        # Menggunakan SMTP_SSL untuk port 465 (Lebih stabil)
        with smtplib.SMTP_SSL("smtp.gmail.com", 465, timeout=15) as server:
            
            server.login(SEND_EMAIL, SEND_PASSWORD)
            server.sendmail(SEND_EMAIL, email, message.as_string())

        return jsonify({"status": True, "msg": f"Email berhasil dikirim ke {email}"})

    except smtplib.SMTPAuthenticationError:
        return jsonify({"error": "Gagal login. Cek App Password/Email"}), 401
    except Exception as e:
        print(f"Detail Error: {str(e)}") # Cek log terminal
        return jsonify({"error": "Terjadi kesalahan pada server"}), 500

if __name__ == "__main__":
    # Mengambil port dari Railway, jika tidak ada default ke 5000
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
