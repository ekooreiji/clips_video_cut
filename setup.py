"""
Setup - Script de Instalação

Sistema CLI/GUI para automatizar cortes de vídeos.
"""

from setuptools import setup, find_packages
from pathlib import Path

# Ler README
readme_file = Path(__file__).parent / "README.md"
long_description = ""
if readme_file.exists():
    long_description = readme_file.read_text(encoding='utf-8')

setup(
    name="clips-videos",
    version="1.0.0",
    description="Sistema CLI/GUI para automatizar cortes de vídeos",
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="Video Clips Team",
    author_email="team@clips-videos.local",
    url="https://github.com/user/clips_videos",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    python_requires=">=3.10",
    install_requires=[
        "click>=8.2.1",
        "PyQt6>=6.0.0",
        "opencv-python>=4.10.0",
        "imageio>=2.31.0",
        "imageio-ffmpeg>=0.4.9",
        "ffmpeg-python>=0.2.0",
        "scipy>=1.11.0",
        "openai-whisper>=20250625",
        "torch>=2.0.0",
        "tiktoken>=0.12.0",
        "numba>=0.60.0",
        "numpy>=1.24.0",
        "tqdm>=4.66.0",
        "python-dateutil>=2.8.0",
        "colorama>=0.4.6",
    ],
    extras_require={
        "dev": [
            "pytest>=7.0.0",
            "pytest-cov>=4.0.0",
            "black>=23.0.0",
            "flake8>=6.0.0",
            "mypy>=1.0.0",
        ],
    },
    entry_points={
        "console_scripts": [
            "clip-tool=cli.commands:cli",
        ],
    },
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: End Users/Desktop",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
    ],
    keywords="video cut clips automation ffmpeg whisper",
    project_urls={
        "Source": "https://github.com/user/clips_videos",
        "Tracker": "https://github.com/user/clips_videos/issues",
    },
)