"""
Functions for working with files: saving and loading JSON.
"""

import json
from pathlib import Path
from typing import Dict, Any
from datetime import datetime

def generate_encrypted_filename() -> str:
    """
    Generate a unique filename with a timestamp in the 'encrypted' folder.
    """
    folder = Path("encrypted")
    folder.mkdir(exist_ok=True)
    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    return str(folder / f"encrypted_{timestamp}.json")

def save_to_file(data: Dict[str, Any], filename: str) -> None:
    """
    Save encrypted data to a JSON file.
    """
    output_path = Path(filename)
    output_path.parent.mkdir(exist_ok=True)
    with open(output_path, "w") as f:
        json.dump(data, f, indent=2)
    print(f"✅ Encrypted data saved to {output_path.absolute()}")

def load_from_file(filename: str) -> Dict[str, Any]:
    """
    Load encrypted data from a JSON file.
    """
    file_path = Path(filename)
    if not file_path.exists():
        raise FileNotFoundError(f"File not found: {file_path}")
    with open(file_path, "r") as f:
        return json.load(f) 