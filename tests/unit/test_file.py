import json
import os
import tempfile
from pathlib import Path

import pytest

from app.utils.file import generate_encrypted_filename, load_from_file, save_to_file


def test_save_load_file():
    """Test saving and loading a file."""
    test_data = {"test": "data", "number": 123}

    with tempfile.NamedTemporaryFile(suffix=".json", delete=False) as temp:
        temp_path = temp.name

    try:
        save_to_file(test_data, temp_path)
        assert os.path.exists(temp_path)
        loaded_data = load_from_file(temp_path)
        assert loaded_data == test_data
    finally:
        if os.path.exists(temp_path):
            os.unlink(temp_path)


def test_load_nonexistent_file():
    """Test that loading a nonexistent file raises FileNotFoundError."""
    nonexistent_path = (
        tempfile.gettempdir()
        + "/nonexistent_file_"
        + str(os.urandom(8).hex())
        + ".json"
    )
    with pytest.raises(FileNotFoundError):
        load_from_file(nonexistent_path)


def test_generate_encrypted_filename():
    """Test filename generation with custom folder."""
    with tempfile.TemporaryDirectory() as tmpdir:
        path = generate_encrypted_filename(folder=tmpdir)
        assert path.startswith(tmpdir)
        assert "encrypted_" in path
        assert path.endswith(".json")
