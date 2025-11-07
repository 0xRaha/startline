from abc import ABC, abstractmethod
from typing import Callable, Dict

class ServerInterface(ABC):
    @abstractmethod
    def start(self, host: str, port: int, app_dispatch: Callable):
        """Start the server."""
        pass

    @abstractmethod
    def stop(self):
        """Gracefully stop the server."""
        pass