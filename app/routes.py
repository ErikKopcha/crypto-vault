import json

from flask import (
    Blueprint,
    flash,
    make_response,
    redirect,
    render_template,
    request,
    url_for,
)

from app.utils.crypto import DEFAULT_ITERATIONS, encrypt
from app.utils.errors import safe_decrypt


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
    if request.args.get("reset") == "true":
        response = make_response(
            render_template(
                "index.html",
                encrypted_data=None,
                decrypted_data=None,
                DEFAULT_ITERATIONS=DEFAULT_ITERATIONS,
            )
        )
        response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
        response.headers["Pragma"] = "no-cache"
        response.headers["Expires"] = "0"
        return response

    encrypted_data = None
    decrypted_data = None

    if request.method == "POST":
        action = request.form.get("action")

        if action == "encrypt":
            data = request.form.get("data", "")
            password = request.form.get("password", "")
            iterations = _parse_iterations()

            if data and password:
                try:
                    encrypted_data = encrypt(data, password, iterations)
                except ValueError as e:
                    flash(str(e))

        elif action == "decrypt":
            password = request.form.get("password", "")

            if not password:
                flash("Password is required for decryption")
                return render_template(
                    "index.html",
                    encrypted_data=None,
                    decrypted_data=None,
                    DEFAULT_ITERATIONS=DEFAULT_ITERATIONS,
                )

            file_provided = (
                "encrypted_file" in request.files
                and request.files["encrypted_file"].filename
            )
            text_provided = request.form.get("encrypted_json", "").strip()

            if file_provided:
                file = request.files["encrypted_file"]
                try:
                    file_content = file.read().decode("utf-8")
                    data = json.loads(file_content)
                    decrypted_data, err = safe_decrypt(data, password)
                    if err:
                        flash(f"Decryption failed: {err}")
                except (UnicodeDecodeError, json.JSONDecodeError):
                    flash("Invalid JSON file format")

            elif text_provided:
                try:
                    data = json.loads(text_provided)
                    decrypted_data, err = safe_decrypt(data, password)
                    if err:
                        flash(f"Decryption failed: {err}")
                except json.JSONDecodeError:
                    flash("Invalid JSON format")

            elif request.form.get("submitted", "") == "true":
                flash("Please provide an encrypted file or JSON data")

    response = make_response(
        render_template(
            "index.html",
            encrypted_data=encrypted_data,
            decrypted_data=decrypted_data,
            DEFAULT_ITERATIONS=DEFAULT_ITERATIONS,
        )
    )
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Pragma"] = "no-cache"
    response.headers["Expires"] = "0"
    return response


@main_bp.route("/reset", methods=["POST"])
def reset():
    """Reset all data and return to clean state."""
    return redirect(url_for("main.index", reset="true"))
