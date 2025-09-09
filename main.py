import csv
import smtplib
import secrets
import string
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# Configuración SMTP
SMTP_SERVER = "mail.ugd.edu.ar"
SMTP_PORT = 587
SMTP_USER = "no-responder@ugd.edu.ar"
SMTP_PASS = "n0.r3sp0nd3r.25"

def generar_contrasena(longitud: int = 12) -> str:
    """
    Genera una contraseña aleatoria con al menos:
    - 1 minúscula, 1 mayúscula, 1 dígito, 1 símbolo seguro.
    """
    letras_min = string.ascii_lowercase
    letras_may = string.ascii_uppercase
    digitos = string.digits
    simbolos = "!@#$%^&*()-_=+?."
    alfabeto = letras_min + letras_may + digitos + simbolos

    # garantizar requisitos mínimos
    base = [
        secrets.choice(letras_min),
        secrets.choice(letras_may),
        secrets.choice(digitos),
        secrets.choice(simbolos),
    ]
    # completar hasta longitud
    base += [secrets.choice(alfabeto) for _ in range(max(0, longitud - len(base)))]
    # mezclar
    secrets.SystemRandom().shuffle(base)
    return "".join(base)

# Conexión SMTP
server = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
server.starttls()
server.login(SMTP_USER, SMTP_PASS)

with open("usuarios.csv", newline="", encoding="utf-8") as f:
    reader = csv.DictReader(f)
    for row in reader:
        cuenta = (row.get("email") or "").strip()
        nueva_pass = (row.get("password") or "").strip()

        if not cuenta:
            # si no hay email, saltar fila
            print("Fila sin 'email'. Se omite.")
            continue

        # si no hay contraseña en el CSV, generar una
        if not nueva_pass:
            nueva_pass = generar_contrasena(12)

        # Crear mensaje
        msg = MIMEMultipart()
        msg["From"] = "Universidad Gastón Dachary <no-responder@ugd.edu.ar>"
        msg["To"] = cuenta
        msg["Subject"] = "Aviso de restablecimiento de contraseña"

        cuerpo = f"""
Estimado/a,

Se restableció la contraseña de su cuenta institucional {cuenta}.
La nueva contraseña es: {nueva_pass}

Para evitar inconvenientes en el uso del servicio de correo, se recomienda no cambiar la contraseña.

Atentamente,
Universidad Gastón Dachary
""".strip()
        msg.attach(MIMEText(cuerpo, "plain"))

        # Enviar
        server.sendmail(SMTP_USER, cuenta, msg.as_string())
        print(f"Correo enviado a {cuenta}")

server.quit()
