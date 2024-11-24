"""
Imitatus - A sophisticated mock HTTP server for development and testing

Imitatus (Latin for "imitation") provides a powerful way to simulate HTTP services
with precision and flexibility. Built with zero external dependencies, it offers
a lightweight yet feature-rich solution for mocking HTTP services.

Features:
    - Token-based authentication system
    - Full HTTP method coverage (GET, POST, PUT, DELETE, etc.)
    - Intelligent in-memory state management
    - Request logging and analytics
    - CORS support out of the box
    - Built with zero external dependencies

Example:
    >>> from imitatus.server import run_server
    >>> run_server(port=8000)
"""

__title__ = "imitatus"
__version__ = "0.1.1"
__author__ = "Serkan Altuntas"
__email__ = "serkan@serkan.ai"
__license__ = "MIT"
__copyright__ = "Copyright 2024 Serkan Altuntas"
__url__ = "https://github.com/serkanaltuntas/imitatus"
__description__ = "A sophisticated mock HTTP server for development and testing"

from .server import run_server

__all__ = ["run_server"]
