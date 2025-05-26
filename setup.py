"""
Package setup configuration for grok-lab
"""

from setuptools import setup, find_packages

setup(
  name="grok-lab",
  version="0.1.0",
  author="Dmitri Zaitsev",
  author_email="dmitri14@gmail.com",
  description="A client library for interacting with Grok-3 API",
  long_description=open("README.md").read(),
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
