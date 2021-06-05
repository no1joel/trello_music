from typing import Any, Dict, Iterator, List

from card import Card, CardAttachment


class CardDeserializer:
    def _card(self, data: Dict[str, Any]) -> Card:
        card_id = data["id"]
        name = data["name"]
        desc = data["desc"]
        short_url = data["shortUrl"]
        attachments_data = data["attachments"]
        assert isinstance(attachments_data, list)
        attachments = list(self._attachments(attachments_data))

        return Card(
            id=card_id,
            name=name,
            desc=desc,
            short_url=short_url,
            attachments=attachments,
        )

    def _cards(self, data: List[Any]) -> Iterator[Card]:
        for card_data in data:
            assert isinstance(card_data, dict)
            yield self._card(card_data)

    def _attachments(self, data: List[Dict[str, str]]) -> Iterator[CardAttachment]:
        for attachment_data in data:
            yield self._attachment(attachment_data)

    def _attachment(self, data: Dict[str, str]) -> CardAttachment:
        url = data["url"]

        return CardAttachment(url=url)

    def from_json(self, data: Any) -> List[Card]:
        assert isinstance(data, list)

        return list(self._cards(data))
