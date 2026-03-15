import json

import pytest

from app.utils.crypto import encrypt


def test_index_get(client):
    """GET / returns 200 with form."""
    response = client.get("/")
    assert response.status_code == 200
    assert b"Encrypt" in response.data
    assert b"Decrypt" in response.data


def test_encrypt_post(client):
    """POST encrypt returns encrypted data."""
    response = client.post(
        "/",
        data={
            "action": "encrypt",
            "data": "secret message",
            "password": "testpass",
            "iterations": "100000",
        },
        follow_redirects=True,
    )
    assert response.status_code == 200
    assert b"encrypted" in response.data.lower() or b"Encrypted Result" in response.data


def test_decrypt_post(client):
    """POST decrypt with valid data returns decrypted text."""
    encrypted = encrypt("hello world", "mypassword")
    response = client.post(
        "/",
        data={
            "action": "decrypt",
            "encrypted_json": json.dumps(encrypted),
            "password": "mypassword",
            "submitted": "true",
        },
        follow_redirects=True,
    )
    assert response.status_code == 200
    assert b"hello world" in response.data


def test_decrypt_wrong_password(client):
    """POST decrypt with wrong password shows error."""
    encrypted = encrypt("secret", "right")
    response = client.post(
        "/",
        data={
            "action": "decrypt",
            "encrypted_json": json.dumps(encrypted),
            "password": "wrong",
            "submitted": "true",
        },
        follow_redirects=True,
    )
    assert response.status_code == 200
    assert b"Invalid password" in response.data or b"failed" in response.data.lower()


def test_reset_post(client):
    """POST /reset redirects to index with reset param."""
    response = client.post("/reset", follow_redirects=False)
    assert response.status_code == 302
    assert "reset=true" in response.location
