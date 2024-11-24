from setuptools import setup, find_packages
from pathlib import Path

this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text()

setup(
    name="imitatus",
    version="0.1.1",
    author="Serkan Altuntas",
    author_email="serkan@serkan.ai",
    description="A sophisticated mock HTTP server for development and testing",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/serkanaltuntas/imitatus",
    project_urls={
        "Bug Tracker": "https://github.com/serkanaltuntas/imitatus/issues",
        "Documentation": "https://github.com/serkanaltuntas/imitatus/docs",
        "Source Code": "https://github.com/serkanaltuntas/imitatus",
    },
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    classifiers=[
        "Development Status :: 5 - Production/Stable",

        "Intended Audience :: Developers",
        "Intended Audience :: Information Technology",

        "Topic :: Internet :: WWW/HTTP :: HTTP Servers",
        "Topic :: Internet :: WWW/HTTP :: Dynamic Content",
        "Topic :: Software Development :: Testing",
        "Topic :: Software Development :: Libraries :: Python Modules",

        "Topic :: Security :: Cryptography",
        "Topic :: System :: Logging",

        "Environment :: Web Environment",
        "Environment :: No Input/Output Interaction",

        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",

        "Operating System :: OS Independent",
        "Natural Language :: English",
    ],
    python_requires=">=3.8",
    install_requires=[],  # Explicitly empty - no production dependencies
    extras_require={
        "dev": [
            "pytest>=7.0.0",
            "pytest-cov>=3.0.0",
            "black>=22.0.0",
            "isort>=5.0.0",
            "flake8>=4.0.0",
            "mypy>=0.900",
        ],
        "docs": [
            "sphinx>=4.0.0",
            "sphinx-rtd-theme>=1.0.0",
        ],
    },
    entry_points={
        "console_scripts": [
            "imitatus=imitatus.server:run_server",
        ],
    },
    include_package_data=True,
    zip_safe=False,
    keywords=[
        "http",
        "server",
        "mock",
        "testing",
        "development",
        "api",
        "rest",
        "zero-dependency",
        "lightweight",
    ],
)
