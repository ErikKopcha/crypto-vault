import pytest

from app.utils.validation import validate_encrypted_payload


def test_validate_encrypted_payload_valid():
    """Valid payload passes validation."""
    payload = {
        "salt": "a" * 32,
        "iv": "b" * 24,
        "encrypted": "c" * 32,
        "iterations": 100000,
    }
    result = validate_encrypted_payload(payload)
    assert result == payload


def test_validate_encrypted_payload_not_dict():
    """Non-dict raises ValueError."""
    with pytest.raises(ValueError, match="must be a JSON object"):
        validate_encrypted_payload("not a dict")


def test_validate_encrypted_payload_missing_keys():
    """Missing required keys raises ValueError."""
    with pytest.raises(ValueError, match="missing keys"):
        validate_encrypted_payload({"salt": "aa", "iv": "bb"})


def test_validate_encrypted_payload_invalid_hex():
    """Invalid hex in salt/iv/encrypted raises ValueError."""
    payload = {
        "salt": "zz",
        "iv": "b" * 24,
        "encrypted": "c" * 32,
        "iterations": 100000,
    }
    with pytest.raises(ValueError, match="must be hex string"):
        validate_encrypted_payload(payload)


def test_validate_encrypted_payload_invalid_iterations():
    """Invalid iterations raises ValueError."""
    payload = {
        "salt": "a" * 32,
        "iv": "b" * 24,
        "encrypted": "c" * 32,
        "iterations": "not_an_int",
    }
    with pytest.raises(ValueError, match="iterations"):
        validate_encrypted_payload(payload)


def test_validate_encrypted_payload_iterations_below_minimum():
    """Iterations below the minimum KDF policy are rejected."""
    from config import MIN_ITERATIONS

    payload = {
        "salt": "a" * 32,
        "iv": "b" * 24,
        "encrypted": "c" * 32,
        "iterations": MIN_ITERATIONS - 1,
    }
    with pytest.raises(ValueError, match="at least"):
        validate_encrypted_payload(payload)


def test_validate_encrypted_payload_iterations_exceeds_max():
    """Iterations exceeding MAX_ITERATIONS raises ValueError (DoS prevention)."""
    from config import MAX_ITERATIONS

    payload = {
        "salt": "a" * 32,
        "iv": "b" * 24,
        "encrypted": "c" * 32,
        "iterations": MAX_ITERATIONS + 1,
    }
    with pytest.raises(ValueError, match="must not exceed"):
        validate_encrypted_payload(payload)
