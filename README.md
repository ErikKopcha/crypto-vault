# CryptoVault

CryptoVault — a simple and secure tool for encrypting and decrypting your sensitive data using AES-256-GCM encryption.

## Requirements

- Python 3.6+
- cryptography package

## Installation

### Setting Up a Virtual Environment (Recommended)

For macOS and other systems with externally managed Python environments, it's recommended to use a virtual environment:

```
# Create a virtual environment
python3 -m venv venv

# Activate the virtual environment
source venv/bin/activate  # On macOS/Linux
# or
venv\Scripts\activate     # On Windows

# Install the required dependency
pip install cryptography

# When done, you can deactivate the environment
# deactivate
```

### Direct Installation

If your Python environment allows direct installations:

```
pip install cryptography
```

## Usage

### Encrypting Data

To encrypt a string:

```
python main.py encrypt "your secret data" "your password"
```

By default, each encrypted file will be saved in the `encrypted/` folder with a unique timestamped filename, for example:

```
encrypted/encrypted_2024-05-23_15-30-12.json
```

You can also specify a custom output file:
```
python main.py encrypt "your secret data" "your password" --output myfile.json
```

### Decrypting Data

To decrypt data from a JSON file:

```
python main.py decrypt encrypted/encrypted_2024-05-23_15-30-12.json "your password"
```

This will display the decrypted text on the console.

### Command-Line Help

For full usage information:

```
python main.py --help
python main.py encrypt --help
python main.py decrypt --help
```

## Security Features

- Uses AES-256-GCM for authenticated encryption
- PBKDF2 key derivation with 100,000 iterations (customizable)
- Randomly generated salt and initialization vector for each encryption
- Proper error handling for authentication failures

## Example

```
# Encrypt some data
python main.py encrypt "This is a secret message" "mysecurepassword"
# Result: encrypted/encrypted_2024-05-23_15-30-12.json

# Encrypt with custom output file
python main.py encrypt "This is a secret message" "mysecurepassword" --output secret.json

# Decrypt the data
python main.py decrypt encrypted/encrypted_2024-05-23_15-30-12.json "mysecurepassword" 