"""
Unit tests for the file utility module.
"""

import os
import json
import tempfile
from pathlib import Path
import pytest
from app.utils.file import save_to_file, load_from_file

def test_save_load_file():
    """Test saving and loading a file."""
    test_data = {"test": "data", "number": 123}
    
    # Create a temporary file for testing
    with tempfile.NamedTemporaryFile(suffix='.json', delete=False) as temp:
        temp_path = temp.name
    
    try:
        # Save data to the file
        save_to_file(test_data, temp_path)
        
        # Verify the file exists
        assert os.path.exists(temp_path)
        
        # Load data from the file
        loaded_data = load_from_file(temp_path)
        
        # Verify loaded data matches original
        assert loaded_data == test_data
    finally:
        # Clean up the temporary file
        if os.path.exists(temp_path):
            os.unlink(temp_path)

def test_load_nonexistent_file():
    """Test that loading a nonexistent file raises FileNotFoundError."""
    # Generate a path to a file that doesn't exist
    nonexistent_path = tempfile.gettempdir() + "/nonexistent_file_" + str(os.urandom(8).hex()) + ".json"
    
    # Verify loading a nonexistent file raises FileNotFoundError
    with pytest.raises(FileNotFoundError):
        load_from_file(nonexistent_path)