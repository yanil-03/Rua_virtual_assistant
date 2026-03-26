"""
setup.py for RUA — makes `python -m rua.main` work from the alexa/ folder.
Also lets you install as editable: pip install -e .
"""

from setuptools import setup, find_packages

setup(
    name="rua",
    version="1.0.0",
    description="RUA – Real life Universal Assistant",
    packages=find_packages(),
    python_requires=">=3.10",
    install_requires=[
        "speechrecognition>=3.10.0",
        "pyttsx3>=2.90",
        "requests>=2.31.0",
        "google-generativeai>=0.5.0",
        "pyaudio>=0.2.14",
    ],
    entry_points={
        "console_scripts": [
            "rua=rua.main:run",
        ],
    },
)
