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
python -m src.server --port 8000
```

## Basic Usage

1. Start the server:
```bash
python -m src.server
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

## Development

### Prerequisites
- Python 3.8+
- pip

### Development Setup
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements-dev.txt
```

### Running Tests
```bash
python -m pytest tests/
```

## Contributing

We welcome contributions! Please see our [Contributing Guidelines](docs/CONTRIBUTING.md) for details.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Author

Created by [Serkan Altuntas](https://serkan.ai)

## Support

- Submit issues via GitHub
- Review documentation

---
Built with precision by Serkan Altuntas