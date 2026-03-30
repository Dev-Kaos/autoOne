# core_mail.py
import smtplib
from email.message import EmailMessage
import config

def enviar_correo_masivo(correo_usuario, password_usuario, cuerpo_mensaje):
    msg = EmailMessage()
    msg['Subject'] = "Informe Semanal de Área - Automatizado"
    msg['From'] = correo_usuario
    msg['To'] = ", ".join(config.DESTINATARIOS)
    msg.set_content(cuerpo_mensaje)

    # Conexión segura
    with smtplib.SMTP_SSL(config.SMTP_SERVER, config.SMTP_PORT) as server:
        server.login(correo_usuario, password_usuario)
        server.send_message(msg)