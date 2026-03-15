"""
Command-line interface for encryption and decryption utility.
"""

import argparse
import getpass
import sys

from app.utils.crypto import DEFAULT_ITERATIONS, encrypt
from app.utils.errors import safe_decrypt
from app.utils.file import generate_encrypted_filename, load_from_file, save_to_file


def parse_args():
    """Parse command line arguments."""
    parser = argparse.ArgumentParser(
        description="Encrypt or decrypt data using AES-256-GCM",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  Encrypt data:
    python cli.py encrypt "This is secret" "password123"
    python cli.py encrypt "This is secret" --prompt

  Decrypt data:
    python cli.py decrypt encrypted/encrypted_2024-05-23_15-30-12.json "password123"
    python cli.py decrypt encrypted/encrypted_2024-05-23_15-30-12.json --prompt
        """,
    )

    subparsers = parser.add_subparsers(
        dest="mode", help="Operation mode", required=True
    )

    encrypt_parser = subparsers.add_parser("encrypt", help="Encrypt data")
    encrypt_parser.add_argument("data", help="Data to encrypt")
    encrypt_parser.add_argument(
        "password",
        nargs="?",
        default=None,
        help="Encryption password (omit with --prompt)",
    )
    encrypt_parser.add_argument(
        "--prompt",
        action="store_true",
        help="Prompt for password securely (no echo)",
    )
    encrypt_parser.add_argument(
        "-o",
        "--output",
        default=None,
        help="Output file (default: encrypted/encrypted_<timestamp>.json)",
    )
    encrypt_parser.add_argument(
        "-i",
        "--iterations",
        type=int,
        default=DEFAULT_ITERATIONS,
        help=f"PBKDF2 iterations (default: {DEFAULT_ITERATIONS})",
    )

    decrypt_parser = subparsers.add_parser("decrypt", help="Decrypt data")
    decrypt_parser.add_argument("file", help="Encrypted JSON file")
    decrypt_parser.add_argument(
        "password",
        nargs="?",
        default=None,
        help="Decryption password (omit with --prompt)",
    )
    decrypt_parser.add_argument(
        "--prompt",
        action="store_true",
        help="Prompt for password securely (no echo)",
    )

    return parser.parse_args()


def _get_password(args, mode: str) -> str:
    """Resolve password from args or prompt."""
    if args.prompt:
        return getpass.getpass(f"Enter {mode} password: ")
    if args.password is not None and args.password != "":
        return args.password
    print("❌ Error: Password required. Use --prompt or provide as argument.")
    sys.exit(1)


def main():
    """Main CLI entry point."""
    args = parse_args()
    try:
        if args.mode == "encrypt":
            password = _get_password(args, "encryption")
            result = encrypt(args.data, password, args.iterations)
            if args.output:
                save_to_file(result, args.output)
            else:
                filename = generate_encrypted_filename()
                save_to_file(result, filename)
        elif args.mode == "decrypt":
            password = _get_password(args, "decryption")
            data = load_from_file(args.file)
            decrypted, err = safe_decrypt(data, password)
            if err:
                print(f"❌ Decryption failed: {err}")
                return 1
            print("✅ Decrypted:")
            print(decrypted)
    except FileNotFoundError as e:
        print(f"❌ Error: {e}")
        return 1
    except ValueError as e:
        print(f"❌ Error: {e}")
        return 1
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
