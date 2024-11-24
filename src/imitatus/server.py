from http.server import HTTPServer, BaseHTTPRequestHandler
import json
import uuid
from urllib.parse import parse_qs, urlparse
import time
from http import HTTPStatus


class MockHTTPRequestHandler(BaseHTTPRequestHandler):
    # Class-level storage
    active_tokens = {}
    items_db = {}
    request_logs = []

    def _set_headers(self, status_code=200, extra_headers=None):
        self.send_response(status_code)
        self.send_header('Content-Type', 'application/json')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods',
                         'GET, POST, PUT, DELETE, PATCH, HEAD, OPTIONS, TRACE, CONNECT')
        self.send_header('Access-Control-Allow-Headers',
                         'Content-Type, Authorization, X-Requested-With')
        if extra_headers:
            for header, value in extra_headers.items():
                self.send_header(header, value)
        self.end_headers()

    def _get_json_body(self):
        try:
            content_length = int(self.headers.get('Content-Length', 0))
            if content_length > 0:
                body = self.rfile.read(content_length)
                return json.loads(body)
            return {}
        except json.JSONDecodeError:
            return {}

    def _send_response(self, data, status_code=200, extra_headers=None):
        self._set_headers(status_code, extra_headers)
        if data is not None:  # Don't send body for HEAD requests
            self.wfile.write(json.dumps(data, indent=2).encode())

    def _verify_token(self):
        auth_header = self.headers.get('Authorization', '')
        if not auth_header.startswith('Bearer '):
            self._send_response({"error": "No token provided"}, 401)
            return False
        token = auth_header.split(' ')[1]
        if token not in self.active_tokens:
            self._send_response({"error": "Invalid token"}, 401)
            return False
        return True

    def _log_request(self):
        request_data = {
            'timestamp': time.time(),
            'method': self.command,
            'path': self.path,
            'headers': dict(self.headers),
            'client_address': self.client_address[0]
        }
        self.request_logs.append(request_data)

    def do_POST(self):
        self._log_request()
        parsed_path = urlparse(self.path)

        if parsed_path.path == '/api/login':
            body = self._get_json_body()
            if body.get('username') == 'admin' and body.get('password') == 'password':
                token = str(uuid.uuid4())
                user_id = str(uuid.uuid4())
                self.active_tokens[token] = {
                    'user_id': user_id,
                    'created_at': time.time()
                }
                self._send_response({
                    "token": token,
                    "user_id": user_id,
                    "message": "Login successful"
                })
            else:
                self._send_response({"error": "Invalid credentials"}, 401)

        elif parsed_path.path == '/api/items':
            if not self._verify_token():
                return
            body = self._get_json_body()
            item_id = str(uuid.uuid4())
            item = {
                'id': item_id,
                'created_at': time.time(),
                **body
            }
            self.items_db[item_id] = item
            self._send_response({
                "id": item_id,
                "item": item,
                "message": "Item created successfully"
            })

        else:
            self._send_response({"error": "Endpoint not found"}, 404)

    def do_GET(self):
        self._log_request()
        parsed_path = urlparse(self.path)

        if parsed_path.path == '/debug/vars':
            # Special endpoint to view server state
            self._send_response({
                "active_tokens_count": len(self.active_tokens),
                "items_count": len(self.items_db),
                "recent_requests": self.request_logs[-5:]
            })
            return

        if parsed_path.path.startswith('/api/items'):
            if not self._verify_token():
                return

            parts = parsed_path.path.split('/')
            if len(parts) == 3:  # /api/items
                self._send_response({"items": self.items_db})
            elif len(parts) == 4:  # /api/items/{id}
                item_id = parts[3]
                if item_id in self.items_db:
                    self._send_response({"item": self.items_db[item_id]})
                else:
                    self._send_response({"error": "Item not found"}, 404)

    def do_PUT(self):
        self._log_request()
        if not self._verify_token():
            return

        parts = self.path.split('/')
        if len(parts) == 4 and parts[1:3] == ['api', 'items']:
            item_id = parts[3]
            if item_id in self.items_db:
                body = self._get_json_body()
                self.items_db[item_id] = {
                    **self.items_db[item_id],
                    **body,
                    'updated_at': time.time()
                }
                self._send_response({
                    "id": item_id,
                    "item": self.items_db[item_id],
                    "message": "Item updated successfully"
                })
            else:
                self._send_response({"error": "Item not found"}, 404)
        else:
            self._send_response({"error": "Invalid endpoint"}, 404)

    def do_PATCH(self):
        self._log_request()
        if not self._verify_token():
            return

        parts = self.path.split('/')
        if len(parts) == 4 and parts[1:3] == ['api', 'items']:
            item_id = parts[3]
            if item_id in self.items_db:
                body = self._get_json_body()
                self.items_db[item_id].update({
                    **body,
                    'patched_at': time.time()
                })
                self._send_response({
                    "id": item_id,
                    "item": self.items_db[item_id],
                    "message": "Item patched successfully"
                })
            else:
                self._send_response({"error": "Item not found"}, 404)
        else:
            self._send_response({"error": "Invalid endpoint"}, 404)

    def do_DELETE(self):
        self._log_request()
        if not self._verify_token():
            return

        parts = self.path.split('/')
        if len(parts) == 4 and parts[1:3] == ['api', 'items']:
            item_id = parts[3]
            if item_id in self.items_db:
                deleted_item = self.items_db.pop(item_id)
                self._send_response({
                    "id": item_id,
                    "item": deleted_item,
                    "message": "Item deleted successfully"
                })
            else:
                self._send_response({"error": "Item not found"}, 404)
        else:
            self._send_response({"error": "Invalid endpoint"}, 404)

    def do_HEAD(self):
        self._log_request()
        # Similar to GET but without body
        extra_headers = {
            'X-Total-Items': str(len(self.items_db)),
            'X-Active-Tokens': str(len(self.active_tokens))
        }
        self._send_response(None, extra_headers=extra_headers)

    def do_OPTIONS(self):
        self._log_request()
        extra_headers = {
            'Allow': 'GET, POST, PUT, DELETE, PATCH, HEAD, OPTIONS, TRACE, CONNECT',
            'X-API-Version': '1.0',
            'X-Server-Time': str(time.time())
        }
        self._send_response({
            "available_endpoints": [
                "/api/login",
                "/api/items",
                "/api/items/{id}",
                "/debug/vars"
            ],
            "supported_methods": extra_headers['Allow'].split(', ')
        }, extra_headers=extra_headers)

    def do_TRACE(self):
        self._log_request()
        # Echo back the request details
        request_details = {
            'headers': dict(self.headers),
            'method': self.command,
            'path': self.path,
            'protocol_version': self.protocol_version,
            'client_address': self.client_address[0]
        }
        self._send_response(request_details)

    def do_CONNECT(self):
        self._log_request()
        # Simulate a tunnel connection
        if self.path.endswith(':443'):
            self._send_response({
                "message": "CONNECT tunnel established",
                "endpoint": self.path,
                "status": "connected"
            })
        else:
            self._send_response({
                "error": "Can only establish CONNECT tunnel to port 443"
            }, 400)


def run_server(port=8000):
    server_address = ('', port)
    httpd = HTTPServer(server_address, MockHTTPRequestHandler)
    print(f"Starting mock HTTP server on port {port}")
    print(f"Server is ready to accept requests...")
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("\nShutting down the server...")
        httpd.server_close()


if __name__ == "__main__":
    run_server()
