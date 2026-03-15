from typing import Any, Dict


REQUIRED_KEYS = frozenset({"salt", "iv", "encrypted", "iterations"})


def validate_encrypted_payload(data: Any) -> Dict[str, Any]:
    """
    Validate that data has the structure required for decryption.

    @param data - Parsed JSON (dict) from file or form
    @returns The validated dict
    @raises ValueError - If structure is invalid
    """
    if not isinstance(data, dict):
        raise ValueError("Encrypted data must be a JSON object")

    missing = REQUIRED_KEYS - set(data.keys())
    if missing:
        raise ValueError(f"Invalid encryption format: missing keys {missing}")

    for key in ("salt", "iv", "encrypted"):
        val = data[key]
        if (
            not isinstance(val, str)
            or len(val) == 0
            or len(val) % 2 != 0
            or not all(c in "0123456789abcdef" for c in val.lower())
        ):
            raise ValueError(f"Invalid encryption format: {key} must be hex string")

    try:
        iterations = int(data["iterations"])
        if iterations < 1:
            raise ValueError("Invalid encryption format: iterations must be positive")
    except (TypeError, ValueError) as e:
        raise ValueError("Invalid encryption format: iterations must be integer") from e

    return data
