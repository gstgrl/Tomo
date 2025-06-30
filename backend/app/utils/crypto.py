from cryptography.fernet import Fernet
import os

# Recupera la chiave dall'ambiente
KEY = os.getenv("ENCRYPTION_KEY")

if not KEY:
    raise ValueError("ENCRYPTION_KEY non trovata nell'ambiente")

fernet = Fernet(KEY.encode())

def cifra_dato(dato: str) -> str:
    """Cripta una stringa"""
    return fernet.encrypt(dato.encode()).decode()

def decifra_dato(dato_cifrato: str) -> str:
    """Decripta una stringa"""
    return fernet.decrypt(dato_cifrato.encode()).decode()
