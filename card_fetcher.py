from dataclasses import dataclass
from datetime import datetime
from typing import List, Optional

import requests

import settings
from card import Card
from card_deserializer import CardDeserializer


@dataclass
class CardCache:
    cards: List[Card]
    timestamp: datetime

    def __init__(self, cards: List[Card]):
        self.cards = cards
        self.timestamp = datetime.now()


class CardFetcher:
    _buy_cache: Optional[CardCache] = None
    _list_cache: Optional[CardCache] = None
    _cache_time = 600

    def _get_cards(self, buy: bool) -> List[Card]:
        cache = self._buy_cache if buy else self._list_cache

        if cache is not None:
            age = datetime.now() - cache.timestamp
            if age.seconds < self._cache_time:
                return cache.cards

        list_id = settings.BUY_LIST if buy else settings.LISTEN_LIST

        fields = ["id", "name", "desc", "shortUrl"]
        params = {
            "fields": fields,
            "key": settings.KEY,
            "token": settings.TOKEN,
            "attachments": "true",
            "attachment_fields": ["url"],
        }
        url = f"https://api.trello.com/1/lists/{list_id}/cards"
        response = requests.get(url, params)
        json_data = response.json()
        cards = CardDeserializer().from_json(json_data)

        cache = CardCache(cards=cards)
        if buy:
            self._buy_cache = cache
        else:
            self._list_cache = cache

        return cards

    def buy_list(self) -> List[Card]:
        return self._get_cards(buy=True)

    def listen_list(self) -> List[Card]:
        return self._get_cards(buy=False)

    def clear_cache(self) -> None:
        self._buy_cache = None
        self._list_cache = None
