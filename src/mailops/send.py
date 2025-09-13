import csv
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from .utils import load_env, genpass, get_field, env_bool
import os


def send_mail_with_template_vars(csv_file: str, env_path: str, template_path: str, subject: str) -> None:
    """
    Envía correos usando una plantilla con variables. Si falta alguna variable en el CSV, muestra un error y omite ese envío.
    """
    load_env(env_path)
    SMTP_SERVER = os.getenv("SMTP_SERVER")
    SMTP_PORT   = int(os.getenv("SMTP_PORT"))
    SMTP_USER   = os.getenv("SMTP_USER")
    SMTP_PASS   = os.getenv("SMTP_PASS")
    USE_TLS     = env_bool("USE_TLS", True)
    FROM_NAME   = os.getenv("FROM_NAME")
    FROM_EMAIL  = os.getenv("FROM_EMAIL")
    FROM_DISPLAY= f"{FROM_NAME} <{FROM_EMAIL}>"
    PASS_LEN    = int(os.getenv("PASS_LEN", "12"))

    if not (SMTP_USER and SMTP_PASS):
        raise SystemExit("Faltan SMTP_USER/SMTP_PASS en el .env de envío.")

    with open(template_path, encoding="utf-8") as tf:
        template_str = tf.read()
    # Detectar si la plantilla es HTML
    is_html = template_path.lower().endswith('.html')
    mime_type = "html" if is_html else "plain"

    with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
        if USE_TLS:
            server.starttls()
        server.login(SMTP_USER, SMTP_PASS)

        with open(csv_file, newline="", encoding="utf-8") as f:
            for row in csv.DictReader(f):
                to_email = get_field(row, "email")
                if not to_email:
                    print("Fila sin 'email'. Omitida.")
                    continue
                password = get_field(row, "password", "contrasena")
                vars = {**row, "password": password, "email": to_email}
                try:
                    cuerpo = template_str.format(**vars)
                except KeyError as e:
                    print(f"ERROR -> {to_email}: Falta la variable {e} en el CSV. Correo omitido.")
                    continue
                msg = MIMEMultipart()
                msg["From"] = FROM_DISPLAY
                msg["To"] = to_email
                msg["Subject"] = subject
                msg.attach(MIMEText(cuerpo, mime_type))
                try:
                    server.sendmail(FROM_EMAIL, to_email, msg.as_string())
                    print(f"OK -> {to_email}")
                except Exception as e:
                    print(f"ERROR -> {to_email}: {e}")


def send_mail_simple(csv_file: str, env_path: str, template_path: str, subject: str) -> None:
    load_env(env_path)
    SMTP_SERVER = os.getenv("SMTP_SERVER")
    SMTP_PORT   = int(os.getenv("SMTP_PORT"))
    SMTP_USER   = os.getenv("SMTP_USER")
    SMTP_PASS   = os.getenv("SMTP_PASS")
    USE_TLS     = env_bool("USE_TLS", True)
    FROM_NAME   = os.getenv("FROM_NAME")
    FROM_EMAIL  = os.getenv("FROM_EMAIL")
    FROM_DISPLAY= f"{FROM_NAME} <{FROM_EMAIL}>"

    if not (SMTP_USER and SMTP_PASS):
        raise SystemExit("Faltan SMTP_USER/SMTP_PASS en el .env de envío.")

    with open(template_path, encoding="utf-8") as tf:
        template_str = tf.read()
    # Detectar si la plantilla es HTML
    is_html = template_path.lower().endswith('.html')
    mime_type = "html" if is_html else "plain"

    with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
        if USE_TLS:
            server.starttls()
        server.login(SMTP_USER, SMTP_PASS)

        with open(csv_file, newline="", encoding="utf-8") as f:
            for row in csv.DictReader(f):
                to_email = get_field(row, "email")
                if not to_email:
                    print("Fila sin 'email'. Omitida.")
                    continue
                msg = MIMEMultipart()
                msg["From"] = FROM_DISPLAY
                msg["To"] = to_email
                msg["Subject"] = subject
                msg.attach(MIMEText(template_str, mime_type))
                try:
                    server.sendmail(FROM_EMAIL, to_email, msg.as_string())
                    print(f"OK -> {to_email}")
                except Exception as e:
                    print(f"ERROR -> {to_email}: {e}")
