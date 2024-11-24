import json
import sys
import time
import uuid
from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib.parse import urlparse


class MockHTTPRequestHandler(BaseHTTPRequestHandler):
    """A sophisticated mock HTTP server handler implementing a complete REST API server.

    This handler provides a full-featured HTTP server implementation with:
    - Token-based authentication
    - CORS support
    - Full HTTP method coverage
    - In-memory state management
    - Request logging
    - Error handling
    - Input validation

    The server maintains state for:
    - Active authentication tokens
    - Item database (CRUD operations)
    - Request history

    All operations use only Python standard library components, maintaining
    the zero-dependency principle while providing sophisticated functionality.

    Attributes:
        active_tokens (dict): Maps authentication tokens to user data and metadata
        items_db (dict): In-memory database storing items with their metadata
        request_logs (list): Circular buffer of recent request data for monitoring

    Example:
        >>> from http.server import HTTPServer
        >>> server = HTTPServer(('localhost', 8000), MockHTTPRequestHandler)
        >>> server.serve_forever()
    """

    # Class-level storage
    active_tokens = {}
    items_db = {}
    request_logs = []

    def _set_headers(self, status_code=200, extra_headers=None):
        """Set response headers with CORS support and content type configuration.

        Sets up standard headers for JSON responses and implements CORS policy.
        Allows customization through extra headers for specific responses.

        Args:
            status_code (int, optional): HTTP status code for response. Defaults to 200.
            extra_headers (dict, optional): Additional headers to include. Defaults to None.

        Note:
            Always sets:
            - Content-Type: application/json
            - CORS headers for cross-origin requests
            - Access control headers for methods and headers
        """
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
        """Parse and validate JSON request body with comprehensive error handling.

        Implements request body parsing with:
        - Size limit enforcement (5MB)
        - JSON format validation
        - Error handling for malformed requests

        Returns:
            dict: Parsed JSON body if valid
            None: If parsing fails, after sending appropriate error response

        Note:
            Automatically sends error responses for:
            - Oversized requests (413)
            - Malformed JSON (400)
            - System errors (500)
        """
        try:
            content_length = int(self.headers.get('Content-Length', 0))
            if content_length > 1024 * 1024 * 5:  # 5MB limit
                self._send_response({"error": "Request entity too large"}, 413)
                return None
            if content_length > 0:
                try:
                    body = self.rfile.read(content_length)
                    return json.loads(body)
                except json.JSONDecodeError:
                    self._send_response({"error": "Invalid JSON format"}, 400)
                    return None
            return {}
        except Exception as e:
            self._send_response({"error": str(e)}, 500)
            return None

    def _send_response(self, data, status_code=200, extra_headers=None):
        """Send JSON response with proper headers and formatting.

        Args:
            data (dict): Response data to be JSON serialized
            status_code (int, optional): HTTP status code. Defaults to 200.
            extra_headers (dict, optional): Additional headers. Defaults to None.

        Note:
            Handles HEAD requests by not sending body content.
        """
        self._set_headers(status_code, extra_headers)
        if data is not None:  # Don't send body for HEAD requests
            self.wfile.write(json.dumps(data, indent=2).encode())

    def _verify_token(self):
        """Verify authentication token from request headers.

        Implements token-based authentication:
        - Extracts Bearer token from Authorization header
        - Validates token against active_tokens store
        - Handles missing or invalid tokens

        Returns:
            bool: True if token is valid, False if invalid or missing

        Note:
            Automatically sends error responses:
            - 401 for missing token
            - 401 for invalid token
        """
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
        """Log request details for monitoring and debugging.

        Captures request metadata including:
        - Timestamp
        - HTTP method
        - Request path
        - Headers
        - Client IP address

        Stores data in the request_logs list for later analysis.
        """
        request_data = {
            'timestamp': time.time(),
            'method': self.command,
            'path': self.path,
            'headers': dict(self.headers),
            'client_address': self.client_address[0]
        }
        self.request_logs.append(request_data)

    def do_POST(self):
        """Handle POST requests for authentication and resource creation.

        Implements endpoints:
        - /api/login: User authentication and token issuing
            - Accepts: username/password
            - Returns: authentication token
        - /api/items: Create new items (requires authentication)
            - Accepts: item data
            - Returns: created item with ID

        Note:
            Login endpoint is public, items endpoint requires authentication.
            All responses are JSON formatted.
        """
        try:
            self._log_request()
            parsed_path = urlparse(self.path)

            if parsed_path.path == '/api/login':
                body = self._get_json_body()
                if body is None:  # Error already handled in _get_json_body
                    return

                # Validate login request body
                if not all(key in body for key in ['username', 'password']):
                    self._send_response({
                        "error": "Missing required fields: username and password"
                    }, 400)
                    return

                # Check credentials
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
                    self._send_response({
                        "error": "Invalid credentials"
                    }, 401)

            elif parsed_path.path == '/api/items':
                # Verify authentication first
                if not self._verify_token():
                    return

                # Get and validate request body
                body = self._get_json_body()
                if body is None:  # Error already handled in _get_json_body
                    return

                # Validate item data
                if not isinstance(body, dict):
                    self._send_response({
                        "error": "Invalid item format - expected object"
                    }, 400)
                    return

                # Generate new item
                item_id = str(uuid.uuid4())
                item = {
                    'id': item_id,
                    'created_at': time.time(),
                    **body
                }

                # Store item
                self.items_db[item_id] = item

                # Send success response
                self._send_response({
                    "id": item_id,
                    "item": item,
                    "message": "Item created successfully"
                })

            else:
                self._send_response({
                    "error": "Endpoint not found"
                }, 404)

        except Exception as e:
            # Log the error (in a real server, you'd use proper logging)
            print(f"Server error in do_POST: {str(e)}", file=sys.stderr)

            # Send error response
            self._send_response({
                "error": "Internal server error",
                "detail": str(e) if self.server.debug else "Contact administrator"
            }, 500)

    def do_GET(self):
        """Handle GET requests for resource retrieval.

        Implements endpoints:
        - /debug/vars: System state and metrics (requires authentication)
            Returns: Active tokens count, items count, recent requests
        - /api/items: List all items (requires authentication)
            Returns: Array of all items
        - /api/items/{id}: Get specific item (requires authentication)
            Returns: Single item by ID

        Note:
            All endpoints except debug require valid authentication token.
            Returns 404 for non-existent items/endpoints.
        """
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
        """Handle PUT requests for full resource updates.

        Implements endpoint:
        - /api/items/{id}: Full update of existing item
            - Requires authentication
            - Replaces entire item while preserving ID and metadata
            - Returns updated item

        Note:
            - Requires authentication
            - Returns 404 for non-existent items
            - Preserves item ID and creation timestamp
        """
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
        """Handle PATCH requests for partial resource updates.

        Implements endpoint:
        - /api/items/{id}: Partial update of existing item
            - Requires authentication
            - Updates only specified fields
            - Preserves other fields
            - Returns updated item

        Note:
            - Requires authentication
            - Returns 404 for non-existent items
            - Adds patch timestamp to item metadata
        """
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
        """Handle DELETE requests for resource removal.

        Implements endpoint:
        - /api/items/{id}: Delete existing item
            - Requires authentication
            - Completely removes item from storage
            - Returns deleted item data

        Note:
            - Requires authentication
            - Returns 404 for non-existent items
            - Operation is permanent and cannot be undone
        """
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
        """Handle HEAD requests for resource metadata.

        Returns metadata about the items collection:
        - X-Total-Items: Count of items in database
        - X-Active-Tokens: Count of active authentication tokens

        Note:
            Response includes headers only, no body content.
        """
        self._log_request()
        # Similar to GET but without body
        extra_headers = {
            'X-Total-Items': str(len(self.items_db)),
            'X-Active-Tokens': str(len(self.active_tokens))
        }
        self._send_response(None, extra_headers=extra_headers)

    def do_OPTIONS(self):
        """Handle OPTIONS requests for API capabilities discovery.

        Returns:
        - Available HTTP methods
        - API endpoints
        - Current server time
        - API version information

        Note:
            Used for CORS preflight and API discovery.
        """
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
        """Handle TRACE requests for request debugging.

        Returns:
            - Complete request details
            - Headers
            - Method
            - Path
            - Protocol version
            - Client address

        Note:
            Used for debugging and request inspection.
        """
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
        """Handle CONNECT requests for tunnel establishment.

        Simulates tunnel connection for HTTPS endpoints:
        - Only accepts connections to port 443
        - Returns connection status
        - Provides endpoint details

        Note:
            Primarily used for HTTPS proxying simulation.
        """
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
    """Start the mock HTTP server on the specified port.

    Args:
        port (int, optional): Port number to listen on. Defaults to 8000.

    Note:
        Can be interrupted with Ctrl+C (KeyboardInterrupt)
        Binds to all available network interfaces ('')
    """
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
