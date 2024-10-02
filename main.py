from flask import Flask, request
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email.mime.text import MIMEText
from email import encoders
import schedule
import time
import threading
from dotenv import load_dotenv
import os

app = Flask(__name__)

# Cargar variables de entorno desde el archivo .env
load_dotenv()

pdf_path = "./pdf/EXAMPLE_MAIL.pdf"
recipient_email = "mila2012@hotmail.es"

def send_email():
    try:
        sender_email = os.getenv('SENDER_MAIL')
        sender_password = os.getenv('SENDER_PASS')
        subject = "Prueba de mail"
        body = "Adjunto encontrarás el PDF generado."

        msg = MIMEMultipart()
        msg['From'] = sender_email
        msg['To'] = recipient_email
        msg['Subject'] = subject
        msg.attach(MIMEText(body, 'plain'))

        with open(pdf_path, "rb") as attachment:
            part = MIMEBase('application', 'octet-stream')
            part.set_payload(attachment.read())
            encoders.encode_base64(part)
            part.add_header('Content-Disposition', f"attachment; filename= {pdf_path}")
            msg.attach(part)

        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(sender_email, sender_password)
        text = msg.as_string()
        server.sendmail(sender_email, recipient_email, text)
        server.quit()
    except Exception as e:
        print(f"Error al enviar el correo: {e}")

def schedule_emails():
    schedule.every().day.at("11:39").do(send_email)

    def run_scheduler():
        while True:
            try:
                schedule.run_pending()
                time.sleep(1)
            except Exception as e:
                print(f"Error en el programador: {e}")

    threading.Thread(target=run_scheduler).start()

# Llama a la función schedule_emails al iniciar el servidor
schedule_emails()

@app.route('/mails', methods=['POST'])
def trigger_schedule():
    schedule_emails()
    return "Programación de correos establecida"

if __name__ == '__main__':
    app.run(debug=True)
