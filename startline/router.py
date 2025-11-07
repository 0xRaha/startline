class Route:
    def __init__(self, path, handler, methods):
        self.path = path
        self.handler = handler
        self.methods = methods

class Router:
    def __init__(self):
        self.routes = []

    def add_route(self, path, handler, methods):
        self.routes.append(Route(path, handler, methods))

    def match(self, path, method):
        # iterate routes, match path parts, return handler or None
        pass