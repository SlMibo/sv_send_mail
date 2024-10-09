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
from datetime import datetime, timedelta
import threading
import logging
logging.basicConfig(level=logging.INFO)

app = Flask(__name__)

# Cargar variables de entorno desde el archivo .env
load_dotenv()

recipient_email = ["mila2012@hotmail.es", "mdelosab@gmail.com"]

scheduler_initialized = False  # Variable de control para evitar múltiples inicializaciones
last_sent_time = datetime.min  # Inicializar con una fecha muy antigua
email_interval = timedelta(minutes=5)  # Ajusta esto según sea necesario

def send_email():
    global last_sent_time
    try:
        current_time = datetime.now()
        if current_time - last_sent_time < email_interval:
            logging.info("Correo ya enviado recientemente. Esperando para el próximo envío.")
            return

        last_sent_time = current_time
        logging.info("Enviando correo...")  # Añadido para ver cuándo se llama a la función
        sender_email = os.getenv('SENDER_MAIL')
        sender_password = os.getenv('SENDER_PASS')
        subject = "Test"
        body = "Adjunto encontrarás el PDF generado."

        msg = MIMEMultipart()
        msg['From'] = sender_email
        msg['To'] = recipient_email
        msg['Subject'] = subject
        msg.attach(MIMEText(body, 'plain'))

        current_date = datetime.now().strftime("%Y%m%d")
        filename1 = f"{current_date} - ReporteDashboard.pdf"
        filename2 = f"{current_date} - ReporteDashboardFyD.pdf"
        pdf_path1 = f"./pdf/{filename1}"
        pdf_path2 = f"./pdf/{filename2}"

        for pdf_path, filename in [(pdf_path1, filename1), (pdf_path2, filename2)]:
            with open(pdf_path, "rb") as attachment:
                part = MIMEBase('application', 'octet-stream')
                part.set_payload(attachment.read())
                encoders.encode_base64(part)
                part.add_header('Content-Disposition', f"attachment; filename={filename}")
                msg.attach(part)
                

        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(sender_email, sender_password)
        text = msg.as_string()
        server.sendmail(sender_email, recipient_email, text)
        server.quit()
        logging.info("Correo enviado.")  # Añadido para ver cuándo se completa el envío
    except Exception as e:
        print(f"Error al enviar el correo: {e}")

def schedule_emails():
    global scheduler_initialized
    if not scheduler_initialized:
        schedule.every().day.at("17:32").do(send_email)

        def run_scheduler():
            while True:
                try:
                    schedule.run_pending()
                    time.sleep(1)
                except Exception as e:
                    print(f"Error en el programador: {e}")

        threading.Thread(target=run_scheduler).start()
        scheduler_initialized = True

@app.route('/mails', methods=['POST'])
def trigger_schedule():
    schedule_emails()
    return "Programación de correos establecida"

if __name__ == '__main__':
    if not app.debug or os.getenv("WERKZEUG_RUN_MAIN") == "true":
        schedule_emails()  # Asegúrate de que solo se ejecuta una vez
    app.run(debug=True, use_reloader=False)