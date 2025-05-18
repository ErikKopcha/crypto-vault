"""
Unit tests for the crypto utility module.
"""

import pytest
from app.utils.crypto import encrypt, decrypt

def test_encrypt_decrypt():
    """Test that encryption followed by decryption returns the original data."""
    original_data = "This is a test message."
    password = "test-password"
    
    # Encrypt the data
    encrypted = encrypt(original_data, password)
    
    # Verify encryption format
    assert "salt" in encrypted
    assert "iv" in encrypted
    assert "encrypted" in encrypted
    assert "iterations" in encrypted
    assert "kdf" in encrypted
    assert "algorithm" in encrypted
    
    # Decrypt the data
    decrypted = decrypt(encrypted, password)
    
    # Verify decryption result
    assert decrypted == original_data

def test_decrypt_wrong_password():
    """Test that decryption with wrong password fails with InvalidTag."""
    from cryptography.exceptions import InvalidTag
    
    original_data = "This is a test message."
    password = "correct-password"
    wrong_password = "wrong-password"
    
    # Encrypt with correct password
    encrypted = encrypt(original_data, password)
    
    # Decrypt with wrong password should raise InvalidTag
    with pytest.raises(InvalidTag):
        decrypt(encrypted, wrong_password) 