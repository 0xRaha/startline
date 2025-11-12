import socket
import select
from .utils import HTTP_STATUS_CODES
from .router import Router
from .request import Request
from .response import Response
from typing import Dict, Callable, Optional
from urllib.parse import parse_qs, unquote


class App:
    """Main application class"""

    def __init__(self):
        self.router = Router()
        self.error_handlers: Dict[int, Callable] = {}

    def route(self, method: str, pattern: str):
        """Generic route decorator"""
        def decorator(handler: Callable):
            self.router.add_route(method, pattern, handler)
            return handler
        return decorator
    
    def get(self, pattern: str):
        return self.router.get(pattern)
    
    def post(self, pattern: str):
        return self.router.post(pattern)
    
    def put(self, pattern: str):
        return self.router.put(pattern)
    
    def delete(self, pattern: str):
        return self.router.delete(pattern)
    
    def use(self, middleware: Callable):
        return self.router.use(middleware)
    
    def error_handler(self, status_code: int):
        """Register custom error handler"""
        def decorator(handler: Callable):
            self.error_handlers[status_code] = handler
            return handler
        return decorator
    
    def parse_request(self, data: bytes) -> Optional[Request]:
        """HTTP request parser"""
        try:
            # Split headers and body
            parts = data.split(b'\r\n\r\n', 1)
            header_data = parts[0].decode('utf-8')
            body = parts[1] if len(parts) > 1 else b''
            
            lines = header_data.split('\r\n')
            request_line = lines[0].split(' ')
            method = request_line[0]
            full_path = request_line[1]
            
            # Parse path and query string
            if '?' in full_path:
                path, query_string = full_path.split('?', 1)
                query_params = parse_qs(query_string)
            else:
                path = full_path
                query_params = {}
            
            path = unquote(path)
            
            # Parse headers
            headers = {}
            for line in lines[1:]:
                if ':' in line:
                    key, value = line.split(':', 1)
                    headers[key.strip().lower()] = value.strip()
            
            return Request(method, path, headers, query_params, body)
        except:
            return None
        
    def build_response(self, response: Response) -> bytes:
        """Build HTTP response bytes"""
        status_msg = HTTP_STATUS_CODES.get(response.status, 'Unknown')

        # Set default header
        if 'Content-Type' not in response.headers:
            response.headers['Content-Type'] = 'text/plain'
            response.headers['Content-Length'] = str(len(response.body))
            response.headers['Server'] = 'Startline/0.1.0'

        # build response
        resp = f'HTTP/1.1 {response.status} {status_msg}\r\n'
        for key, value in response.headers.items():
            resp += f'{key}: {value}\r\n'
        resp += '\r\n'

        return resp.encode('utf-8') + response.body
    
    def handle_request(self, request: Request) -> Response:
        """Route and handle request"""
        # Apply middleware
        for middleware in self.router.middleware:
            result = middleware(request)
            if isinstance(result, Response):
                return result
            
        # Match route
        handler, params = self.router.match(request.method, request.path)

        if handler:
            try:
                result = handler(request, **params)
                if isinstance(result, Response):
                    return result
                if isinstance(result, dict):
                    return Response().json(result)
                if isinstance(result, str):
                    return Response().text(result)
                return Response().text(str(result))
            except Exception as e:
                print(f"Handler error: {e}")
                if 500 in self.error_handlers:
                    return self.error_handlers[500](request, e)
                return Response().json({'error': 'Internal server error'}, 500)
        else:
            if 404 in self.error_handlers:
                return self.error_handlers[404](request)
            return Response().json({'error': 'Not found'}, 404)
        
    def run(self, host: str = '0.0.0.0', port: int = 8000, backlog: int = 128):
        """Run server with epoll/select for high performance"""
        server_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        server_sock.setblocking(False)
        server_sock.bind((host, port))
        server_sock.listen(backlog)

        print("🚀 Startline server rinning on http://{host}:{port}")
        
        try:
            poller = select.epoll()
            READ_ONLY = select.EPOLLIN
            poller.register(server_sock.fileno(), READ_ONLY)
            use_epoll = True
        except:
            poller = select.poll()
            READ_ONLY = select.POLLIN
            poller.register(server_sock.fileno(), READ_ONLY)
            use_epoll = False
        
        connections = {}

        print("📊 Optimized for high throughput")

        try:
            while True:
                events = poller.poll(0.1)
                
                for fd, event in events:
                    if fd == server_sock.fileno():
                        # Accept new connection
                        try:
                            client_sock, addr = server_sock.accept()
                            client_sock.setblocking(False)
                            poller.register(client_sock.fileno(), READ_ONLY)
                            connections[client_sock.fileno()] = client_sock
                        except:
                            pass
                    else:
                        # Handle client request
                        client_sock = connections.get(fd)
                        if client_sock:
                            try:
                                data = client_sock.recv(8192)
                                if data:
                                    request = self.parse_request(data)
                                    if request:
                                        response = self.handle_request(request)
                                        client_sock.sendall(self.build_response(response))
                                
                                poller.unregister(fd)
                                client_sock.close()
                                del connections[fd]
                            except:
                                try:
                                    poller.unregister(fd)
                                    client_sock.close()
                                    del connections[fd]
                                except:
                                    pass
        except KeyboardInterrupt:
            print("\n👋 Shutting down...")
            server_sock.close()