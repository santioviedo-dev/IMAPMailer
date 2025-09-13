import os, csv, requests
from .utils import load_env, genpass, get_field

def _uapi_add_pop(host, user, token, local, domain, password, quota):
    url = f"https://{host}:2083/execute/Email/add_pop"
    headers = {"Authorization": f"cpanel {user}:{token}"}
    data = {"email": local, "domain": domain, "password": password, "quota": str(quota)}
    r = requests.post(url, headers=headers, data=data, timeout=30)
    r.raise_for_status()
    return r.json()

def create_from_csv(csv_file: str, env_path: str) -> None:
    load_env(env_path)

    HOST        = os.getenv("HOST")
    CPANEL_USER = os.getenv("CPANEL_USER")
    CPANEL_TOKEN= os.getenv("CPANEL_TOKEN")
    PASS_LEN    = int(os.getenv("PASS_LEN", "12"))
    QUOTA_DEF   = os.getenv("QUOTA_DEFAULT", "1024")  # MB; "0" = ilimitado
    PASS_DEFAULT    = os.getenv("PASS_DEFAULT", "Temporal2025.")

    if not (HOST and CPANEL_USER and CPANEL_TOKEN):
        raise SystemExit("Faltan HOST/CPANEL_USER/CPANEL_TOKEN en el .env (create).")

    with open(csv_file, newline="", encoding="utf-8") as f:
        for row in csv.DictReader(f):
            email = get_field(row, "email")
            local = get_field(row, "local")
            domain= get_field(row, "domain")
            pw    = get_field(row, "contrasena", "password") or PASS_DEFAULT
            quota = get_field(row, "quota") or QUOTA_DEF

            if email:
                if "@" not in email:
                    print(f"ERROR -> '{email}' inválido")
                    continue
                local, domain = email.split("@", 1)
            if not local or not domain:
                print("Fila sin local@domain. Omitida.")
                continue

            try:
                res = _uapi_add_pop(HOST, CPANEL_USER, CPANEL_TOKEN, local, domain, pw, quota)
                ok = bool(res.get("status") == 1)
                print(f"{'OK' if ok else 'FAIL'} -> {local}@{domain} quota={quota} {res}")
            except Exception as e:
                print(f"ERROR -> {local}@{domain}: {e}")
