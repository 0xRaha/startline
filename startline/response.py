import json
from typing import Dict, Any
from dataclasses import dataclass

@dataclass
class Response:
    """HTTP Response object"""
    status: int = 200
    headers: Dict[str, str] = None
    body: bytes = b''

    def __post_init__(self):
        if self.headers is None:
            self.headers = {}

    def json(self, data: Any, status: int = 200):
        """Return JSON response"""
        self.status = status
        self.body = json.dumps(data).encode('utf-8')
        self.headers['Content-Type'] = 'application/json'
        return self
    
    def text(self, data: str, status: int = 200):
        """Return Text response"""
        self.status = status
        self.body = data.encode('utf-8')
        self.headers['Content-Type'] = 'text/plain'
        return self
    
    def html(self, data: str, status: int = 200):
        """Return HTML response"""
        self.status = status
        self.body = data.encode('utf-8')
        self.hearders['Content-Type'] = 'text/plain'
        return self