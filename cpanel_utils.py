import requests
import config

def set_mail_password(email_local, domain, new_password):
    url = f"https://{config.HOST}:2083/execute/Email/passwd_pop"
    headers = {
        "Authorization": f"cpanel {config.CPANEL_USER}:{config.CPANEL_TOKEN}"
    }
    data = {
        "email": email_local,       # solo la parte antes de @
        "domain": domain,           # ej. ugd.edu.ar
        "password": new_password    # respeta política de contraseñas del servidor
    }
    r = requests.post(url, headers=headers, data=data, timeout=30)
    r.raise_for_status()
    print(r.json())  # debería incluir status: 1 si fue OK

# ejemplo
set_mail_password("prueba.servidores", "ugd.edu.ar", "AbcD!9372$qp")
