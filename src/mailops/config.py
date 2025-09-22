import os
from dotenv import load_dotenv

load_dotenv()

SMTP_SERVER = os.getenv("SMTP_SERVER", "mail.ugd.edu.ar")
SMTP_PORT = int(os.getenv("SMTP_PORT", 587))
SMTP_USER = os.getenv("SMTP_USER")
SMTP_PASS = os.getenv("SMTP_PASS")
USE_TLS= os.getenv("USE_TLS", "true").lower() in ("1", "true", "yes")
CPANEL_TOKEN = os.getenv("CPANEL_TOKEN")
CPANEL_USER = os.getenv("CPANEL_USER", "ugdeduar")
HOST = os.getenv("HOST", "cpanel.ugd.edu.ar")

FROM_NAME   = os.getenv("FROM_NAME", "Universidad Gastón Dachary")
FROM_EMAIL  = os.getenv("FROM_EMAIL", SMTP_USER or "no-responder@ugd.edu.ar")
FROM_DISPLAY= f"{FROM_NAME} <{FROM_EMAIL}>"

CSV_FILE    = os.getenv("CSV_FILE", "usuarios.csv")
SUBJECT = os.getenv("SUBJECT", "Aviso de restablecimiento de contraseña")
BODY_TEMPLATE = os.getenv(
    "CUERPO_TEMPLATE",
    (
        "Estimado/a,\n\n"
        "Se restableció la contraseña de su cuenta institucional {cuenta}.\n"
        "La nueva contraseña es: {contrasena}\n\n"
        "Por motivos de seguridad, cámbiela en su primer inicio de sesión.\n\n"
        "Atentamente,\n"
        "Universidad Gastón Dachary"
    ),
)

PASS_LEN = int(os.getenv("PASS_LEN", "12"))
