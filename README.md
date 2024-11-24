# Imitatus

A sophisticated mock HTTP server for development and testing. Imitatus (Latin for "imitation") provides a powerful way to simulate HTTP services with precision and flexibility.

![Python Version](https://img.shields.io/badge/python-3.8+-blue.svg)
![License](https://img.shields.io/badge/license-MIT-green.svg)

## Features

- 🔐 Token-based authentication system
- 🎯 Full HTTP method coverage (GET, POST, PUT, DELETE, PATCH, HEAD, OPTIONS, TRACE, CONNECT)
- 💾 Intelligent in-memory state management
- 📊 Request logging and analytics
- 🛡️ CORS support out of the box
- 🧪 Ready-to-use test collection
- ⚡ Zero external dependencies

## Quick Start

```bash
# Install
git clone https://github.com/serkanaltuntas/imitatus.git
cd imitatus
pip install -r requirements.txt

# Run
python -m imitatus.server --port 8000
```

## Basic Usage

1. Start the server:
```bash
python -m imitatus.server
```

2. Authenticate:
```bash
curl -X POST http://localhost:8000/api/login \
  -H "Content-Type: application/json" \
  -d '{"username": "admin", "password": "password"}'
```

3. Make requests:
```bash
curl http://localhost:8000/api/items \
  -H "Authorization: Bearer your-token-here"
```

## API Overview

### Authentication
- `POST /api/login`: Get authentication token
```json
{
  "username": "admin",
  "password": "password"
}
```

### Core Endpoints
- `GET /api/items`: List all items
- `POST /api/items`: Create item
- `GET /api/items/{id}`: Get specific item
- `PUT /api/items/{id}`: Full update
- `PATCH /api/items/{id}`: Partial update
- `DELETE /api/items/{id}`: Delete item

### System Endpoints
- `GET /debug/vars`: System state and metrics
- `OPTIONS /api/items`: Available methods and API info

## Dependencies

### Prerequisites
- Python 3.8+
- pip

### Production
Imitatus is designed to have **zero production dependencies**. It uses only Python's standard library components for all core functionality. This design choice provides several benefits:

- 🔒 Enhanced security with no third-party dependency risks
- ⚡ Fast and lightweight installation
- 🎯 No version conflicts with other packages
- 📦 Maximum portability across Python environments

### Development
For development and testing, we use several high-quality tools:

```bash
# Install development dependencies
pip install -r requirements-dev.txt

# Install testing dependencies
pip install -r requirements-test.txt
```

See `requirements-dev.txt` and `requirements-test.txt` for the complete list of development and testing dependencies.


## Contributing

We welcome contributions! Please see our [Contributing Guidelines](CONTRIBUTING.md) for details.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Author

Built with precision by [Serkan Altuntas](https://serkan.ai)

## Support

- Submit issues via GitHub
- Review documentation
