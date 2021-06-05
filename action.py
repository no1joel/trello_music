from typing import Optional
from trello_action import TrelloAction
from dataclasses import dataclass


@dataclass
class Action:
    key: str
    description: str
    trello_action: Optional[TrelloAction]
