import json

from app.utils.crypto import encrypt


def test_index_get(client):
    """GET / returns 200 with form."""
    response = client.get("/")
    assert response.status_code == 200
    assert b"Encrypt" in response.data
    assert b"Decrypt" in response.data


def test_encrypt_post(client):
    """POST encrypt redirects and shows encrypted data once."""
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


def test_encrypt_result_clears_after_refresh(client):
    """Encrypted result is not retained after a GET refresh."""
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
    assert b"Encrypted Result" in response.data

    refresh_response = client.get("/")

    assert refresh_response.status_code == 200
    assert b"Encrypted Result" not in refresh_response.data


def test_decrypt_post(client):
    """POST decrypt with valid data redirects and returns decrypted text once."""
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


def test_decrypt_result_clears_after_refresh(client):
    """Decrypted result is not retained after a GET refresh."""
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
    assert b"hello world" in response.data

    refresh_response = client.get("/")

    assert refresh_response.status_code == 200
    assert b"hello world" not in refresh_response.data


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
