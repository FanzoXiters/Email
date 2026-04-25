from flask import Flask, request, jsonify
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

app = Flask(__name__)

SEND_EMAIL = "EMAIL_KAMU_BENER"
SEND_PASSWORD = "APP_PASSWORD_BENER"

@app.route("/")
def home():
    return "API aktif!"

@app.route("/send", methods=["POST"])
def send():
    try:
        data = request.get_json()

        if not data:
            return jsonify({"error": "Body kosong / bukan JSON"}), 400

        name = data.get("name")
        email = data.get("email")
        subject = data.get("subject")
        body = data.get("body")

        if not all([name, email, subject, body]):
            return jsonify({"error": "Data tidak lengkap"}), 400

        message = MIMEMultipart()
        message["From"] = SEND_EMAIL
        message["To"] = email
        message["Subject"] = subject

        message.attach(MIMEText(body, "html"))

        with smtplib.SMTP("smtp.gmail.com", 587, timeout=10) as server:
            server.starttls()
            server.login(SEND_EMAIL, SEND_PASSWORD)
            server.sendmail(SEND_EMAIL, email, message.as_string())

        return jsonify({"status": True, "msg": "Email terkirim"})

    except Exception as e:
        print("ERROR:", str(e))  # masuk ke logs
        return jsonify({"error": str(e)}), 500


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
