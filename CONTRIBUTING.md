# Contributing to Imitatus

Thanks for your interest in contributing to Imitatus! This project aims to be a sophisticated, zero-dependency mock HTTP server. This guide will help you understand how to contribute effectively.

## Table of Contents

- [Code of Conduct](#code-of-conduct)
- [Getting Started](#getting-started)
  - [Development Environment](#development-environment)
  - [Project Structure](#project-structure)
- [Development Workflow](#development-workflow)
  - [Creating a Feature Branch](#creating-a-feature-branch)
  - [Making Changes](#making-changes)
  - [Testing](#testing)
  - [Code Style](#code-style)
- [Pull Request Process](#pull-request-process)
- [Development Guidelines](#development-guidelines)
- [Release Process](#release-process)

## Code of Conduct

By participating in this project, you agree to maintain a respectful and inclusive environment. Key points:

- Use welcoming and inclusive language
- Be respectful of differing viewpoints and experiences
- Accept constructive criticism gracefully
- Focus on what's best for the project
- Show empathy towards other contributors

## Getting Started

### Development Environment

1. Fork and clone the repository:
   ```bash
   git clone https://github.com/serkanaltuntas/imitatus.git
   cd imitatus
   ```

2. Create a virtual environment:
   ```bash
   python -m venv .venv
   source .venv/bin/activate  # On Windows: .venv\Scripts\activate
   ```

3. Install development dependencies:
   ```bash
   make develop
   # Or manually:
   pip install -r requirements-dev.txt
   pip install -e .
   ```

### Project Structure

```
imitatus/
├── src/imitatus/        # Source code
│   ├── __init__.py      # Package initialization
│   └── server.py        # Core server implementation
├── tests/               # Test suite
│   └── test_server.py   # Server tests
├── examples/            # Usage examples
├── docs/                # Documentation
└── Makefile             # Build and development commands
```

## Development Workflow

### Creating a Feature Branch

1. Ensure you're on the latest main branch:
   ```bash
   git checkout main
   git pull origin main
   ```

2. Create a feature branch:
   ```bash
   git checkout -b feature/feature-name
   ```

### Making Changes

1. Follow the zero-dependency principle:
   - Core functionality should only use Python's standard library
   - Development tools can be added to requirements-dev.txt
   - Test dependencies can be added to requirements-test.txt

2. Document your changes:
   - Add docstrings to new functions and classes
   - Update README.md if adding new features
   - Add examples for significant features

### Testing

1. Run the test suite:
   ```bash
   make test
   ```

2. Run specific test categories:
   ```bash
   make test-unit     # Unit tests only
   make test-api      # API tests only
   make test-coverage # Tests with coverage report
   ```

3. Writing tests:
   - Add tests for all new features
   - Maintain test coverage above 90%
   - Follow existing test patterns in test_server.py

### Code Style

1. Format your code:
   ```bash
   make format    # Runs black and isort
   ```

2. Check style compliance:
   ```bash
   make lint      # Runs flake8, black --check, and isort --check
   ```

3. Style guidelines:
   - Follow PEP 8
   - Use type hints where appropriate
   - Keep functions focused and modular
   - Maintain clear separation of concerns

## Pull Request Process

1. Before submitting:
   - Ensure all tests pass
   - Run code formatting
   - Update documentation
   - Add test cases for new features

2. PR Guidelines:
   - Use a clear, descriptive title
   - Fill out the PR template completely
   - Reference any related issues
   - Keep changes focused and atomic

3. Review process:
   - PRs require approval
   - Address all review comments
   - Maintain a professional, constructive dialogue

## Development Guidelines

1. Zero-dependency principle:
   - Core functionality must use only standard library
   - Document any new standard library usage
   - Justify any development dependency additions

2. Error handling:
   - Use appropriate HTTP status codes
   - Provide clear error messages
   - Log errors appropriately
   - Handle edge cases gracefully

3. Performance considerations:
   - Minimize memory usage
   - Optimize request handling
   - Consider concurrent request handling

4. Security practices:
   - Validate all inputs
   - Sanitize error messages
   - Follow security best practices
   - Don't expose sensitive information

## Release Process

1. Version numbering:
   - Follow semantic versioning (MAJOR.MINOR.PATCH)
   - Document all changes in CHANGELOG.md

2. Release checklist:
   - Update version in __init__.py
   - Update CHANGELOG.md
   - Run full test suite
   - Build and test distribution
   - Create GitHub release
   - Upload to PyPI

3. Release commands:
   ```bash
   make build         # Build distribution
   make publish-test  # Upload to TestPyPI
   make publish       # Upload to PyPI
   ```

Thanks for contributing to Imitatus! Your contributions help make this project better.

For questions or support:
- Open an issue on GitHub
- Contact me (Serkan Altuntas)
- Join project discussions
