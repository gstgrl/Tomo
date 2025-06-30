import bcrypt

# HASH
def hash_dato(dato: str) -> str:
    salt = bcrypt.gensalt()
    hashed = bcrypt.hashpw(dato.encode(), salt)
    return hashed.decode()  # salvabile come stringa nel DB

# VERIFICA
def verifica_dato(dato: str, hash_stored: str) -> bool:
    return bcrypt.checkpw(dato.encode(), hash_stored.encode())
