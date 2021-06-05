from dataclasses import dataclass
from typing import List


@dataclass
class CardAttachment:
    url: str


@dataclass
class Card:
    id: str
    name: str
    desc: str
    short_url: str
    attachments: List[CardAttachment]
