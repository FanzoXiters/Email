import smtplib 
from  flask import Flask, request, jsonify
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart 
send_email = "cikazoexe@gmail.com
#Enter here gmail account app password
send_password = "gmail account app password "

app = Flask(__name__)
@app.route("/send", methods=["POST"])

def send():
  try:
    
    data = request.get_json()
    name = data["name"]
    email = data["name"]
    subject = data["subject"]
    body = data["body"]
    
    message = MIMEMultipart()
    message["From"] = f"{name}<{send_email}>"
    message["To"] = name 
    message["Subject"] = subject 
    message.attach(MIMEText(body, "plain"))
    smtp_server = "smtp.gmail.com"
    port = 587 
   
    with smtplib.SMTP(smtp_server,port) as server:
      
      server.starttls()
      
      server.login(send_email, send_password)
      server.sendmail(send_email, email, message.as_string())
      
      server.quit()
      return jsonify({"status":"true","text":"send msg success"})
  except Exception as e : 
    return jsonify({"status":"false","text":str(e)})


if __name__ == '__main__':
    app.run(debug=True) 
  
  
  
  
  
  
