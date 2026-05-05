import secrets

PAIRING_CODE_ALPHABET = "ABCDEFGHJKLMNPQRSTUVWXYZ23456789"

def generate_pairing_code() -> str:
    raw_code = "".join(secrets.choice(PAIRING_CODE_ALPHABET) for _ in range(8))
    return f"{raw_code[:4]}-{raw_code[4:]}"

def normalize_pairing_code(code: str) -> str:
    return code.replace("-", "").strip().upper()

def format_pairing_code(code: str) -> str:
    normalized_code = normalize_pairing_code(code)
    return f"{normalized_code[:4]}-{normalized_code[4:]}"
