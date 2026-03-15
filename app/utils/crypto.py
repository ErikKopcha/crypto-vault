import os
from typing import Any, Dict

from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.ciphers.aead import AESGCM
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC


DEFAULT_ITERATIONS = 100_000
KEY_LENGTH = 32
SALT_LENGTH = 16
IV_LENGTH = 12

MIN_ITERATIONS = 1_000
MAX_ITERATIONS = 1_000_000


def _validate_iterations(iterations: int) -> None:
    """Validate iterations within safe bounds."""
    if not MIN_ITERATIONS <= iterations <= MAX_ITERATIONS:
        raise ValueError(
            f"Iterations must be between {MIN_ITERATIONS} and {MAX_ITERATIONS}"
        )


def encrypt(
    data: str, password: str, iterations: int = DEFAULT_ITERATIONS
) -> Dict[str, Any]:
    """
    Encrypt data using AES-256-GCM with PBKDF2 key derivation.
    """
    _validate_iterations(iterations)

    salt = os.urandom(SALT_LENGTH)
    iv = os.urandom(IV_LENGTH)
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=KEY_LENGTH,
        salt=salt,
        iterations=iterations,
    )

    key = kdf.derive(password.encode())
    aesgcm = AESGCM(key)
    ciphertext = aesgcm.encrypt(iv, data.encode(), None)

    return {
        "kdf": "pbkdf2",
        "iterations": iterations,
        "algorithm": "aes-256-gcm",
        "salt": salt.hex(),
        "iv": iv.hex(),
        "encrypted": ciphertext.hex(),
    }


def decrypt(data: Dict[str, Any], password: str) -> str:
    """
    Decrypt data that was encrypted with AES-256-GCM.
    """

    try:
        salt = bytes.fromhex(data["salt"])
        iv = bytes.fromhex(data["iv"])
        ciphertext = bytes.fromhex(data["encrypted"])
        iterations = int(data["iterations"])
    except (KeyError, ValueError) as e:
        raise ValueError(f"Invalid encryption format: {str(e)}") from e

    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=KEY_LENGTH,
        salt=salt,
        iterations=iterations,
    )

    key = kdf.derive(password.encode())
    aesgcm = AESGCM(key)
    decrypted = aesgcm.decrypt(iv, ciphertext, None)

    return decrypted.decode()
