#!/bin/bash

# Exit on error
set -e

echo "Setting up the encryption/decryption tool..."

# Create virtual environment if it doesn't exist
if [ ! -d "venv" ]; then
    echo "Creating virtual environment..."
    python3 -m venv venv
    echo "Virtual environment created."
else
    echo "Virtual environment already exists."
fi

# Activate virtual environment
echo "Activating virtual environment..."
source venv/bin/activate

# Install dependencies
echo "Installing dependencies..."
pip install -r requirements.txt

# Create .env file if it doesn't exist
if [ ! -f ".env" ]; then
    echo "Creating .env file..."
    cp .env.example .env
    echo ".env file created. Please update it with your configuration."
else
    echo ".env file already exists."
fi

# Create encrypted directory if it doesn't exist
if [ ! -d "encrypted" ]; then
    echo "Creating encrypted directory..."
    mkdir -p encrypted
    echo "Encrypted directory created."
else
    echo "Encrypted directory already exists."
fi

echo "Setup complete! You can now run the application."
echo "To start the web server: make run"
echo "To use the CLI: python cli.py encrypt \"Your secret\" \"your-password\"" 