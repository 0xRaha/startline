from .router import Router
from .server.interface import ServerInterface

class App:
    def __init__(self, server, ServerInterface=None):
        self.router = Router()
        self.middleware = []  # list of callables
        self.server = server  # default provided by package

    def route(self, path: str, methods=('GET',)):
        def decorator(func):
            self.router.add_route(path, func, methods)
            return func
        return decorator
    
    def dispatch (self, request):
        # run before middleware
        for mid in self.middleware:
            mid.before(request)
        handler = self.router.match(request.path, request.method)
        if handler is None:
            from .exceptions import NotFound
            return NotFound()
        result = handler(request)
        # run after middleware
        for mid in self.middleware:
            mid.after(request, result)
        return result
    
    def run(self, host='127.0.0.1', port=8000):
        if not self.server:
            from .server.socket_server import SocketServer
            self.server = SocketServer()
        self.server.start(host, port, self.dispatch)