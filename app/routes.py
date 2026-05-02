import json

from flask import (
    Blueprint,
    flash,
    make_response,
    redirect,
    render_template,
    request,
    session,
    url_for,
)

from app.utils.crypto import DEFAULT_ITERATIONS, encrypt
from app.utils.errors import safe_decrypt
from config import MAX_DATA_LENGTH, MAX_PASSWORD_LENGTH


main_bp = Blueprint("main", __name__)


def _parse_iterations() -> int:
    """Parse and validate iterations from form."""
    raw = request.form.get("iterations", str(DEFAULT_ITERATIONS))
    try:
        value = int(raw)
    except ValueError:
        return DEFAULT_ITERATIONS
    from app.utils.crypto import MAX_ITERATIONS, MIN_ITERATIONS

    return max(MIN_ITERATIONS, min(MAX_ITERATIONS, value))


@main_bp.route("/", methods=["GET", "POST"])
def index():
    """
    Main route for the encryption/decryption tool.
    """
    encrypted_data = session.pop("encrypted_data", None)
    decrypted_data = session.pop("decrypted_data", None)
    selected_action = session.pop("selected_action", None)

    if request.method == "POST":
        action = request.form.get("action")
        selected_action = action

        if action == "encrypt":
            data = request.form.get("data", "")
            password = request.form.get("password", "")
            iterations = _parse_iterations()

            if len(password) > MAX_PASSWORD_LENGTH:
                flash(f"Password must not exceed {MAX_PASSWORD_LENGTH} characters")
            elif len(data) > MAX_DATA_LENGTH:
                flash(f"Data must not exceed {MAX_DATA_LENGTH:,} characters")
            elif data and password:
                try:
                    session["encrypted_data"] = encrypt(data, password, iterations)
                except ValueError as e:
                    flash(str(e))

        elif action == "decrypt":
            password = request.form.get("password", "")

            if len(password) > MAX_PASSWORD_LENGTH:
                flash(f"Password must not exceed {MAX_PASSWORD_LENGTH} characters")
                session["selected_action"] = selected_action
                return redirect(url_for("main.index"))
            if not password:
                flash("Password is required for decryption")
                session["selected_action"] = selected_action
                return redirect(url_for("main.index"))

            file_provided = (
                "encrypted_file" in request.files
                and request.files["encrypted_file"].filename
            )
            text_provided = request.form.get("encrypted_json", "").strip()

            if text_provided and len(text_provided) > MAX_DATA_LENGTH:
                flash(f"Encrypted data must not exceed {MAX_DATA_LENGTH:,} characters")
            elif file_provided:
                file = request.files["encrypted_file"]
                try:
                    file_content = file.stream.read(MAX_DATA_LENGTH + 1).decode("utf-8")
                    if len(file_content) > MAX_DATA_LENGTH:
                        flash(
                            "Encrypted file content must not exceed "
                            f"{MAX_DATA_LENGTH:,} characters"
                        )
                        session["selected_action"] = selected_action
                        return redirect(url_for("main.index"))
                    data = json.loads(file_content)
                    decrypted_data_result, err = safe_decrypt(data, password)
                    if err:
                        flash(f"Decryption failed: {err}")
                    else:
                        session["decrypted_data"] = decrypted_data_result
                except (UnicodeDecodeError, json.JSONDecodeError):
                    flash("Invalid JSON file format")

            elif text_provided:
                try:
                    data = json.loads(text_provided)
                    decrypted_data_result, err = safe_decrypt(data, password)
                    if err:
                        flash(f"Decryption failed: {err}")
                    else:
                        session["decrypted_data"] = decrypted_data_result
                except json.JSONDecodeError:
                    flash("Invalid JSON format")

            elif request.form.get("submitted", "") == "true":
                flash("Please provide an encrypted file or JSON data")

        session["selected_action"] = selected_action
        return redirect(url_for("main.index"))

    response = make_response(
        render_template(
            "index.html",
            encrypted_data=encrypted_data,
            decrypted_data=decrypted_data,
            selected_action=selected_action,
            DEFAULT_ITERATIONS=DEFAULT_ITERATIONS,
        )
    )
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Pragma"] = "no-cache"
    response.headers["Expires"] = "0"
    return response
