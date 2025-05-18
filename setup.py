"""
Setup script for the encryption/decryption tool.
"""

from setuptools import setup, find_packages

with open('README.md', 'r') as f:
    long_description = f.read()

with open('requirements.txt', 'r') as f:
    requirements = f.read().splitlines()

setup(
    name="crypto_vault",
    version="1.0.0",
    author="Erik K.",
    author_email="",
    description="A secure tool for encrypting and decrypting sensitive data",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/erikkopcha/crypto_vault",
    packages=find_packages(),
    include_package_data=True,
    install_requires=requirements,
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
    entry_points={
        'console_scripts': [
            'encrypt-decrypt=cli:main',
        ],
    },
) 