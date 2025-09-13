import os, csv, requests
from .utils import load_env, genpass, get_field

def _uapi_passwd_pop(host, user, token, local, domain, password):
    url = f"https://{host}:2083/execute/Email/passwd_pop"
    headers = {"Authorization": f"cpanel {user}:{token}"}
    data = {"email": local, "domain": domain, "password": password}
    r = requests.post(url, headers=headers, data=data, timeout=30)
    r.raise_for_status()
    return r.json()

def reset_from_csv(csv_file: str, env_path: str) -> None:
    load_env(env_path)

    HOST        = os.getenv("HOST")
    CPANEL_USER = os.getenv("CPANEL_USER")
    CPANEL_TOKEN= os.getenv("CPANEL_TOKEN")
    PASS_LEN    = int(os.getenv("PASS_LEN", "12"))

    if not (HOST and CPANEL_USER and CPANEL_TOKEN):
        raise SystemExit("Faltan HOST/CPANEL_USER/CPANEL_TOKEN en el .env de reset.")

    with open(csv_file, newline="", encoding="utf-8") as f:
        for row in csv.DictReader(f):
            email = get_field(row, "email")
            local = get_field(row, "local")
            domain= get_field(row, "domain")
            pw    = get_field(row, "contrasena", "password")

            if email:
                if "@" not in email:
                    print(f"ERROR -> '{email}' inválido")
                    continue
                local, domain = email.split("@", 1)
            if not local or not domain:
                print("Fila sin local@domain. Omitida.")
                continue
            if not pw:
                pw = genpass(PASS_LEN)

            try:
                res = _uapi_passwd_pop(HOST, CPANEL_USER, CPANEL_TOKEN, local, domain, pw)
                ok = bool(res.get("status") == 1)
                print(f"{'OK' if ok else 'FAIL'} -> {local}@{domain} {res}")
            except Exception as e:
                print(f"ERROR -> {local}@{domain}: {e}")
