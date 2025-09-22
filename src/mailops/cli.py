import argparse
from pathlib import Path
from .send import  send_mail_with_template_vars, send_mail_simple
from .reset import reset_from_csv
from .create import create_from_csv
from .utils import ensure_passwords
from .config import PASS_LEN

ROOT = Path(__file__).resolve().parents[2]
DEFAULT_ENV_SEND  = ROOT / ".env.send"
DEFAULT_ENV_RESET = ROOT / ".env.reset"   # también para create

def main():
    p = argparse.ArgumentParser(prog="mailops")
    sub = p.add_subparsers(dest="cmd", required=True)

    ps = sub.add_parser("send", help="Enviar correos personalizados desde CSV")
    ps.add_argument("--csv", required=True)
    ps.add_argument("--env", default=str(DEFAULT_ENV_SEND))
    ps.add_argument("--template", required=True, help="Ruta a la plantilla de correo")
    ps.add_argument("--subject", required=True, help="Asunto del correo")
    ps.add_argument("--simple", action="store_true", help="Enviar correo sin variables, solo el texto de la plantilla")

    pr = sub.add_parser("reset", help="Restablecer contraseñas vía cPanel UAPI")
    pr.add_argument("--csv", required=True)
    pr.add_argument("--env", default=str(DEFAULT_ENV_RESET))

    pc = sub.add_parser("create", help="Crear cuentas de correo vía cPanel UAPI")
    pc.add_argument("--csv", required=True)
    pc.add_argument("--env", default=str(DEFAULT_ENV_RESET))

    a = p.parse_args()
    if a.cmd == "send":
        if a.simple:
            send_mail_simple(a.csv, a.env, a.template, a.subject)
        else:
            ensure_passwords(a.csv, PASS_LEN)
            send_mail_with_template_vars(a.csv, a.env, a.template, a.subject)
    elif a.cmd == "reset":
        reset_from_csv(a.csv, a.env)
    else:
        create_from_csv(a.csv, a.env)

if __name__ == "__main__":
    main()
