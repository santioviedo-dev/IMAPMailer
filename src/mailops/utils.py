import os, secrets, string, csv
from dotenv import load_dotenv

def load_env(path: str) -> None:
    load_dotenv(path)  # no borra variables existentes

def env_bool(name: str, default: bool) -> bool:
    v = os.getenv(name)
    return default if v is None else v.lower() in ("1","true","yes")

def genpass(n: int = 12) -> str:
    low, up, dig, sym = string.ascii_lowercase, string.ascii_uppercase, string.digits, "!@#$%^&*()-_=+?."
    alphabet = low + up + dig + sym
    base = [secrets.choice(low), secrets.choice(up), secrets.choice(dig), secrets.choice(sym)]
    base += [secrets.choice(alphabet) for _ in range(max(0, n - 4))]
    secrets.SystemRandom().shuffle(base)
    return "".join(base)

def get_field(row: dict, *keys: str) -> str:
    for k in keys:
        v = (row.get(k) or "").strip()
        if v:
            return v
    return ""

def ensure_passwords(csv_file: str, pass_len: int) -> None:
    rows = []
    with open(csv_file, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        fieldnames = reader.fieldnames or []
        # asegurar que exista la columna "password"
        if "password" not in fieldnames:
            fieldnames.append("password")

        for row in reader:
            if not row.get("password") and not row.get("contrasena"):
                row["password"] = genpass(pass_len)
            elif row.get("contrasena") and not row.get("password"):
                # normalizar a la misma clave
                row["password"] = row["contrasena"]
            rows.append(row)

    # sobrescribir el CSV con las contraseñas completadas
    with open(csv_file, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)
