from app.utils.crypto import encrypt
from app.utils.errors import safe_decrypt
from config import MAX_ITERATIONS


def test_safe_decrypt_success():
    """Successful decryption returns (result, None)."""
    encrypted = encrypt("secret", "password")
    result, err = safe_decrypt(encrypted, "password")
    assert result == "secret"
    assert err is None


def test_safe_decrypt_wrong_password():
    """Wrong password returns (None, error_message)."""
    encrypted = encrypt("secret", "password")
    result, err = safe_decrypt(encrypted, "wrong")
    assert result is None
    assert "Invalid password" in err or "corrupted" in err


def test_safe_decrypt_invalid_format():
    """Invalid payload structure returns (None, error_message)."""
    result, err = safe_decrypt({"invalid": "data"}, "password")
    assert result is None
    assert err is not None


def test_safe_decrypt_iterations_exceeds_max():
    """Payload with iterations > MAX returns (None, error_message) — DoS prevention."""
    payload = {
        "salt": "a" * 32,
        "iv": "b" * 24,
        "encrypted": "c" * 32,
        "iterations": MAX_ITERATIONS + 1,
    }
    result, err = safe_decrypt(payload, "password")
    assert result is None
    assert "must not exceed" in err
