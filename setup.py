"""
Setup script for the Cart-ONDC package.
"""

from setuptools import setup, find_packages
import os

# Read the contents of the README file
with open("UPDATED_README.md", encoding="utf-8") as f:
    long_description = f.read()

# Read the version from cart_ondc/__init__.py
about = {}
with open(os.path.join("cart_ondc", "__init__.py"), encoding="utf-8") as f:
    exec(f.read(), about)

setup(
    name="cart-ondc",
    version=about["__version__"],
    description="A WhatsApp-based solution for onboarding sellers to ONDC",
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="Cart-ONDC Team",
    author_email="example@example.com",
    url="https://github.com/yourusername/cart-ondc",
    packages=find_packages(),
    install_requires=[
        "Flask>=3.1.0",
        "firebase-admin>=6.6.0",
        "google-cloud-firestore>=2.20.0",
        "requests>=2.32.3",
        "python-dotenv>=1.0.1",
    ],
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
    ],
    python_requires=">=3.8",
) 