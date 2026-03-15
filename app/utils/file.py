import json
import logging
from datetime import datetime
from pathlib import Path
from typing import Any, Dict

from config import DEFAULT_ENCRYPTED_FOLDER


logger = logging.getLogger(__name__)


def generate_encrypted_filename(folder: str = DEFAULT_ENCRYPTED_FOLDER) -> str:
    """
    Generate a unique filename with a timestamp in the encrypted folder.

    @param folder - Output folder name (default from config)
    """
    path = Path(folder)
    path.mkdir(exist_ok=True)
    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    return str(path / f"encrypted_{timestamp}.json")


def save_to_file(data: Dict[str, Any], filename: str) -> None:
    """
    Save encrypted data to a JSON file.
    """
    output_path = Path(filename)
    output_path.parent.mkdir(parents=True, exist_ok=True)

    with open(output_path, "w") as f:
        json.dump(data, f, indent=2)

    logger.info("Encrypted data saved to %s", output_path.absolute())
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
