#!/usr/bin/env python3
"""
DATASOPH AI - Setup Configuration
World's most intelligent AI data scientist with advanced RAG, authentication & conversation memory
"""

from setuptools import setup, find_packages
import os

# Read the README file
def read_readme():
    with open("README.md", "r", encoding="utf-8") as fh:
        return fh.read()

# Read requirements
def read_requirements():
    with open("requirements.txt", "r", encoding="utf-8") as fh:
        return [line.strip() for line in fh if line.strip() and not line.startswith("#")]

setup(
    name="datasoph-ai",
    version="1.0.0",
    author="Datasoph AI Team",
    author_email="team@datasoph.ai",
    description="World's most intelligent AI data scientist with advanced RAG, authentication & conversation memory",
    long_description=read_readme(),
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/datasoph-ai",
    project_urls={
        "Bug Tracker": "https://github.com/yourusername/datasoph-ai/issues",
        "Documentation": "https://docs.datasoph.ai",
        "Homepage": "https://datasoph.ai",
    },
    packages=find_packages(exclude=["tests*", "docs*"]),
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Developers",
        "Intended Audience :: Science/Research",
        "Topic :: Scientific/Engineering :: Artificial Intelligence",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.9",
    install_requires=read_requirements(),
    extras_require={
        "dev": [
            "pytest>=7.4.0",
            "pytest-asyncio>=0.21.0",
            "pytest-cov>=4.1.0",
            "black>=23.0.0",
            "flake8>=6.0.0",
            "mypy>=1.5.0",
            "pre-commit>=3.3.0",
        ],
        "docs": [
            "sphinx>=7.1.0",
            "sphinx-rtd-theme>=1.3.0",
            "myst-parser>=2.0.0",
        ],
        "deployment": [
            "gunicorn>=21.2.0",
            "uvicorn[standard]>=0.23.0",
            "docker>=6.1.0",
        ]
    },
    entry_points={
        "console_scripts": [
            "datasoph-backend=backend.app.main:main",
            "datasoph-web=web_app.streamlit_app:main",
            "datasoph-rag=rag_system.cli:main",
        ],
    },
    include_package_data=True,
    package_data={
        "": ["*.txt", "*.md", "*.yml", "*.yaml", "*.json"],
    },
    zip_safe=False,
    keywords=[
        "ai",
        "data-science",
        "machine-learning",
        "rag",
        "langchain",
        "fastapi",
        "streamlit",
        "flutter",
        "authentication",
        "firebase",
        "chromadb",
        "openrouter",
        "conversational-ai"
    ],
) 