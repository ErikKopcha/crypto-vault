# Secure Encryption/Decryption Tool

A secure tool for encrypting and decrypting sensitive data using strong cryptography.

## Features

- Encrypt data using AES-256-GCM with PBKDF2 key derivation
- Decrypt encrypted data using a password
- Web interface for easy use
- Command-line interface for automation
- All processing happens locally for maximum security
- No data is stored or logged

## Project Structure

```
encrypt_decrypt/
│
├── app/                        # Main application package
│   ├── __init__.py             # Flask app initialization
│   ├── routes.py               # Route definitions
│   ├── utils/                  # Utility modules
│   │   ├── __init__.py
│   │   ├── crypto.py           # Cryptographic functions
│   │   └── file.py             # File handling functions
│   │
│   ├── static/                 # Static assets
│   │   ├── css/
│   │   │   └── styles.css      # Application styles
│   │   └── js/
│   │       └── script.js       # JavaScript functionality
│   │
│   └── templates/              # Jinja2 templates
│       └── index.html          # Main page template
│
├── encrypted/                  # Default directory for encrypted files
├── tests/                      # Test files
├── scripts/                    # Utility scripts
├── archive/                    # Archived files
├── config.py                   # Application configuration
├── run.py                      # Web application entry point
├── cli.py                      # Command-line interface
├── setup.py                    # Package installation configuration
├── Makefile                    # Build automation
├── pytest.ini                  # PyTest configuration
└── requirements.txt            # Project dependencies
```

## Installation

1. Clone the repository:
   ```
   git clone https://github.com/yourusername/encrypt_decrypt.git
   cd encrypt_decrypt
   ```

2. Create and activate a virtual environment:
   ```
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install the dependencies:
   ```
   pip install -r requirements.txt
   ```

4. Alternative: Install as a package (provides encrypt-decrypt command):
   ```
   pip install -e .
   ```

## macOS Installation and Usage

1. Ensure you have Python 3.6+ installed:
   ```
   python3 --version
   ```

2. If needed, install Python using Homebrew:
   ```
   brew install python
   ```

3. Create and activate a virtual environment:
   ```
   python3 -m venv venv
   source venv/bin/activate
   ```

4. Install the dependencies:
   ```
   pip3 install -r requirements.txt
   ```
   
   Make sure you install all required packages:
   ```
   pip3 install python-dotenv flask cryptography
   ```

5. Start the application:
   ```
   python3 run.py
   ```

6. For the CLI tool:
   ```
   python3 cli.py encrypt "Your secret message" "your-password"
   python3 cli.py decrypt encrypted/encrypted_YYYY-MM-DD_HH-MM-SS.json "your-password"
   ```

## Usage

### Web Interface

1. Start the web server:
   ```
   python run.py
   ```

2. Open a browser and go to `http://localhost:5000`

3. Use the interface to:
   - Encrypt: Enter text, provide a password, set iterations (optional), and click "Encrypt"
   - Decrypt: Upload an encrypted file or paste encrypted JSON, enter the password, and click "Decrypt"

### Command Line

For encryption:
```
python cli.py encrypt "Your secret message" "your-password"
```

For decryption:
```
python cli.py decrypt encrypted/encrypted_YYYY-MM-DD_HH-MM-SS.json "your-password"
```

If installed as a package:
```
encrypt-decrypt encrypt "Your secret message" "your-password"
encrypt-decrypt decrypt encrypted/encrypted_YYYY-MM-DD_HH-MM-SS.json "your-password"
```

Additional options:
```
python cli.py encrypt --help
python cli.py decrypt --help
```

### Makefile

The project includes a Makefile with helpful commands:
```
make help        # Show available commands
make test        # Run tests
make lint        # Check code style
```

## Security

- Uses AES-256-GCM for authenticated encryption
- PBKDF2 with SHA-256 for key derivation
- Default 100,000 iterations for key derivation (adjustable)
- No data is stored or transmitted over the network
- All processing happens locally in your browser or on your machine

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Disclaimer

This tool is provided for legitimate security purposes. Always use encryption responsibly and in compliance with applicable laws and regulations.