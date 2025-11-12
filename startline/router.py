import re
from typing import Dict, List, Tuple, Callable, Optional

class Router:
    """Fast Regex-Based Router"""
    def __init__(self):
        self.routes: Dict[str, List[Tuple[re.Pattern, Callable]]] = {
            'GET': [], 'POST': [], 'PUT': [], 'DELETE': [], 'PATCH': []
        }
        self.middleware = List[Callable] = []

    def add_route(self, method: str, pattern: str, handler: Callable):
        """Add a route with parameter support"""
        # Convert /user/:id to regex pattern
        regex_pattern = re.sub(r':(\w+)', r'(?P<\1>[^/]+)', pattern)
        regex_pattern = f'^{regex_pattern}$'
        compiled = re.compile(regex_pattern)
        self.route[method].append((compiled, handler))

    def get(self, pattern: str):
        """Decorator for GET routes"""
        def decorator(handler: Callable):
            self.add_route('GET', pattern, handler)
            return handler
        return decorator

    def post(self, pattern: str):
        """Decorator for POST routes"""
        def decorator(handler: Callable):
            self.add_route('POST', pattern, handler)
            return handler
        return decorator

    def put(self, pattern: str):
        """Decorator for PUT routes"""
        def decorator(handler: Callable):
            self.add_route('PUT', pattern, handler)
            return handler
        return decorator

    def delete(self, pattern: str):
        """Decorator for DELETE routes"""
        def decorator(handler: Callable):
            self.add_route('DELETE', pattern, handler)
            return handler
        return decorator

    def use(self, middleware: Callable):
        """Add middleware"""
        self.middleware.append(middleware)
        return middleware
    
    def match(self, method: str, path: str) -> Optional[Tuple[Callable, Dict]]:
        """Match route and extract parameters"""
        for pattern, handler in self.routes.get(method, []):
            match = pattern.match(path)
            if match:
                return handler, match.groupdict()
            return None, {}