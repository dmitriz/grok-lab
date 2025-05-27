"""
Package setup configuration for grok-lab
"""

from setuptools import setup, find_packages
from pathlib import Path

# Read the contents of README.md
this_directory = Path(__file__).parent
with open(this_directory / "README.md", encoding="utf-8") as f:
    long_description = f.read()

setup(
  name="grok-lab",
  version="0.1.0",
  author="Dmitri Zaitsev",
  author_email="dmitri14@gmail.com",
  description="A client library for interacting with Grok-3 API",
  long_description=long_description,
  long_description_content_type="text/markdown",
  url="https://github.com/dmitriz/grok-lab",
  packages=find_packages(),
  py_modules=["grok_api"],  # Include the module directly
  classifiers=[
    "Programming Language :: Python :: 3",
    "License :: OSI Approved :: MIT License",
    "Operating System :: OS Independent",
  ],
  python_requires=">=3.8",
  install_requires=[
    "requests>=2.25.0",
  ],
)
