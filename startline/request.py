import json
from typing import Dict, List, Optional
from dataclasses import dataclass

@dataclass
class Request:
    """HTTP Request object"""
    method: str
    path: str
    headers: Dict[str, str]
    query_params: Dict[str, List[str]]
    body: bytes

    @property
    def json(self) -> Optional[Dict]:
        """Parse JSON body"""
        try:
            return json.loads(self.body.decode('utf-8'))
        except:
            return None