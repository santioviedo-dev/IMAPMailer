import csv
import smtplib
import secrets
import string
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import config


def generar_contrasena(longitud: int = config.PASS_LEN) -> str:
    """Genera una contraseña aleatoria segura."""
    letras_min = string.ascii_lowercase
    letras_may = string.ascii_uppercase
    digitos = string.digits
    simbolos = "!@#$%^&*()-_=+?."
    alfabeto = letras_min + letras_may + digitos + simbolos

    base = [
        secrets.choice(letras_min),
        secrets.choice(letras_may),
        secrets.choice(digitos),
        secrets.choice(simbolos),
    ]
    base += [secrets.choice(alfabeto) for _ in range(max(0, longitud - len(base)))]
    secrets.SystemRandom().shuffle(base)
    return "".join(base)


server = smtplib.SMTP(config.SMTP_SERVER, config.SMTP_PORT)
if config.USE_TLS:
    server.starttls()
server.login(config.SMTP_USER, config.SMTP_PASS)

with open(config.CSV_FILE, newline="", encoding="utf-8") as f:
    reader = csv.DictReader(f)
    for row in reader:
        cuenta = (row.get("email") or "").strip()
        nueva_pass = (row.get("password") or "").strip()

        if not cuenta:
            print("Fila sin 'email'. Se omite.")
            continue

        if not nueva_pass:
            nueva_pass = generar_contrasena()

        msg = MIMEMultipart()
        msg["From"] = config.FROM_DISPLAY
        msg["To"] = cuenta
        msg["Subject"] = config.SUBJECT

        cuerpo = config.CUERPO_TEMPLATE.format(
            cuenta=cuenta,
            contrasena=nueva_pass
        )
        msg.attach(MIMEText(cuerpo, "plain"))

        server.sendmail(config.FROM_EMAIL, cuenta, msg.as_string())
        print(f"Correo enviado a {cuenta}")

server.quit()
