import hashlib


def generate_public_id(real_id):
    """
    Gera um public_id único baseado no id real usando SHA256.
    """
    secret = "cyber_secret_2025"
    return hashlib.sha256(f"{secret}_{real_id}".encode()).hexdigest()
