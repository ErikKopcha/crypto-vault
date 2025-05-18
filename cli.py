"""
Command-line interface for encryption and decryption utility.
"""

import sys
import argparse
from cryptography.exceptions import InvalidTag
from app.utils.crypto import encrypt, decrypt, DEFAULT_ITERATIONS
from app.utils.file import save_to_file, load_from_file, generate_encrypted_filename

def parse_args():
    """Parse command line arguments."""
    parser = argparse.ArgumentParser(
        description="Encrypt or decrypt data using AES-256-GCM",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  Encrypt data:
    python cli.py encrypt "This is secret" "password123"
  
  Decrypt data:
    python cli.py decrypt encrypted/encrypted_2024-05-23_15-30-12.json "password123"
        """
    )
    
    subparsers = parser.add_subparsers(dest="mode", help="Operation mode", required=True)
    
    # Encrypt command
    encrypt_parser = subparsers.add_parser("encrypt", help="Encrypt data")
    encrypt_parser.add_argument("data", help="Data to encrypt")
    encrypt_parser.add_argument("password", help="Encryption password")
    encrypt_parser.add_argument(
        "-o", "--output", 
        default=None, 
        help=f"Output file (default: encrypted/encrypted_<timestamp>.json)"
    )
    encrypt_parser.add_argument(
        "-i", "--iterations", 
        type=int, 
        default=DEFAULT_ITERATIONS, 
        help=f"PBKDF2 iterations (default: {DEFAULT_ITERATIONS})"
    )
    
    # Decrypt command
    decrypt_parser = subparsers.add_parser("decrypt", help="Decrypt data")
    decrypt_parser.add_argument("file", help="Encrypted JSON file")
    decrypt_parser.add_argument("password", help="Decryption password")
    
    return parser.parse_args()

def main():
    """Main CLI entry point."""
    args = parse_args()
    try:
        if args.mode == "encrypt":
            result = encrypt(args.data, args.password, args.iterations)
            if args.output:
                save_to_file(result, args.output)
            else:
                filename = generate_encrypted_filename()
                save_to_file(result, filename)
        elif args.mode == "decrypt":
            data = load_from_file(args.file)
            try:
                decrypted = decrypt(data, args.password)
                print("✅ Decrypted:")
                print(decrypted)
            except InvalidTag:
                print("❌ Decryption failed: Invalid password or corrupted data")
                return 1
            except ValueError as e:
                print(f"❌ Decryption failed: {str(e)}")
                return 1
    except FileNotFoundError as e:
        print(f"❌ Error: {str(e)}")
        return 1
    except Exception as e:
        print(f"❌ Unexpected error: {str(e)}")
        return 1
    return 0

if __name__ == "__main__":
    sys.exit(main()) 