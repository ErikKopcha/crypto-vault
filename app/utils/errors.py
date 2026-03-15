from typing import Any, Optional, Tuple

from cryptography.exceptions import InvalidTag

from app.utils.crypto import decrypt
from app.utils.validation import validate_encrypted_payload


INVALID_PASSWORD_MSG = "Invalid password or corrupted data"


def safe_decrypt(data: Any, password: str) -> Tuple[Optional[str], Optional[str]]:
    """
    Decrypt with validation and unified error handling.

    @param data - Parsed JSON (dict) or raw structure
    @param password - Decryption password
    @returns (decrypted_string, None) on success; (None, error_message) on failure
    """
    try:
        validated = validate_encrypted_payload(data)
        result = decrypt(validated, password)
        return result, None
    except InvalidTag:
        return None, INVALID_PASSWORD_MSG
    except ValueError as e:
        return None, str(e)
