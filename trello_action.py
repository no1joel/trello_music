from dataclasses import dataclass
from typing import Any, Dict


@dataclass
class TrelloAction:
    request_data: Dict[str, Any]
