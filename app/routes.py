"""
Route definitions for the application.
"""

import json
from flask import Blueprint, render_template, request, flash, redirect, url_for, session, make_response
from app.utils.crypto import encrypt, decrypt, DEFAULT_ITERATIONS
from cryptography.exceptions import InvalidTag

# Create blueprint
main_bp = Blueprint('main', __name__)

@main_bp.route("/", methods=["GET", "POST"])
def index():
    """
    Main route for the encryption/decryption tool.
    """
    # If reset parameter is present, don't show any data
    if request.args.get('reset') == 'true':
        response = make_response(render_template("index.html", 
                                encrypted_data=None, 
                                decrypted_data=None,
                                DEFAULT_ITERATIONS=DEFAULT_ITERATIONS))
        # Add no-cache headers
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
            iterations = int(request.form.get("iterations", DEFAULT_ITERATIONS))
            
            if data and password:
                encrypted_data = encrypt(data, password, iterations)
        
        elif action == "decrypt":
            password = request.form.get("password", "")
            
            if not password:
                flash("Password is required for decryption")
                return render_template("index.html")
            
            # Check if user actually tried to submit data for decryption
            file_provided = 'encrypted_file' in request.files and request.files['encrypted_file'].filename
            text_provided = request.form.get("encrypted_json", "").strip()
            
            if file_provided:
                # Option 1: File upload
                file = request.files['encrypted_file']
                try:
                    file_content = file.read().decode('utf-8')
                    data = json.loads(file_content)
                    decrypted_data = decrypt(data, password)
                except (UnicodeDecodeError, json.JSONDecodeError):
                    flash("Invalid JSON file format")
                except InvalidTag:
                    flash("Decryption failed: Invalid password or corrupted data")
                except ValueError as e:
                    flash(f"Decryption failed: {str(e)}")
            
            elif text_provided:
                # Option 2: JSON text input
                try:
                    data = json.loads(text_provided)
                    decrypted_data = decrypt(data, password)
                except (InvalidTag, ValueError, json.JSONDecodeError) as e:
                    flash(f"Decryption failed: {str(e)}")
            
            elif request.form.get('submitted', '') == 'true':
                # Only show error if user actually clicked the Decrypt button
                flash("Please provide an encrypted file or JSON data")
    
    response = make_response(render_template("index.html", 
                            encrypted_data=encrypted_data, 
                            decrypted_data=decrypted_data,
                            DEFAULT_ITERATIONS=DEFAULT_ITERATIONS))
    
    # Add cache control headers to all responses
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Pragma"] = "no-cache"
    response.headers["Expires"] = "0"
    
    return response

@main_bp.route("/reset", methods=["POST"])
def reset():
    """
    Reset all data and return to clean state.
    """
    return redirect(url_for('main.index', reset='true')) 