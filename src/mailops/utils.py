import os, secrets, string
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
