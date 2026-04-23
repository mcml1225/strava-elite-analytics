"""
Setup script for Strava Elite Analytics Platform
"""

from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

with open("requirements.txt", "r", encoding="utf-8") as fh:
    requirements = [line.strip() for line in fh if line.strip() and not line.startswith("#")]

setup(
    name="strava-elite-analytics",
    version="1.0.0",
    author="Your Name",
    author_email="your.email@example.com",
    description="Data science platform for analyzing elite athletes on Strava",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/strava-elite-analytics",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.8",
    install_requires=requirements,
    entry_points={
        "console_scripts": [
            "strava-analytics=main:main",
        ],
    },
)