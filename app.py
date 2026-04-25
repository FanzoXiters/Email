from flask import Flask, request, jsonify
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import os

app = Flask(__name__)

# ambil dari environment biar aman
SEND_EMAIL = os.environ.get("EMAIL_USER")
SEND_PASSWORD = os.environ.get("EMAIL_PASS")

@app.route("/")
def home():
    return "API aktif!"

@app.route("/send", methods=["POST"])
def send():
    try:
        data = request.get_json()

        name = data["name"]
        email = data["email"]
        subject = data["subject"]
        body = data["body"]

        message = MIMEMultipart()
        message["From"] = f"{name} <{SEND_EMAIL}>"
        message["To"] = email
        message["Subject"] = subject

        message.attach(MIMEText(body, "html"))

        with smtplib.SMTP("smtp.gmail.com", 587) as server:
            server.starttls()
            server.login(SEND_EMAIL, SEND_PASSWORD)
            server.sendmail(SEND_EMAIL, email, message.as_string())

        return jsonify({"status": True, "msg": "Email terkirim"})

    except Exception as e:
        return jsonify({"status": False, "error": str(e)})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)