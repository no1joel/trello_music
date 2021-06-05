"""Return a random trello from the stuff to check out list that I have."""

import sys
from typing import List, Optional, Sequence

import numpy
import requests

import settings
from action import Action
from card import Card
from card_deserializer import CardDeserializer
from trello_action import TrelloAction

KEY = settings.KEY
TOKEN = settings.TOKEN
LISTEN_LIST = settings.LISTEN_LIST
BUY_LIST = settings.BUY_LIST

ACTIONS: List[Action] = [
    Action("k", "[K]eep", None),
    Action("a", "[A]rchive", TrelloAction({"closed": True})),
    Action("b", "[B]uy (later)", TrelloAction({"idList": BUY_LIST})),
    Action("t", "Move to [t]op", TrelloAction({"pos": "top"})),
    Action("q", "[Q]uit", None),
]


def print_safe(something: str) -> None:
    """Print a string after encoding / decoding to remove unsafe chars."""
    print(something.encode("ascii", "replace").decode("ascii"))


def get_cards(buy: bool) -> List[Card]:
    """Fetch all cards from the trello list."""
    list_id = BUY_LIST if buy else LISTEN_LIST

    fields = ["id", "name", "desc", "shortUrl"]
    params = {
        "fields": fields,
        "key": KEY,
        "token": TOKEN,
        "attachments": "true",
        "attachment_fields": ["url"],
    }
    url = f"https://api.trello.com/1/lists/{list_id}/cards"
    response = requests.get(url, params)
    json_data = response.json()
    cards = CardDeserializer().from_json(json_data)

    return cards


def get_probabilities(length: int) -> List[float]:
    """Return probabilities for a given length."""

    probabilities = [x ** -1 for x in range(1, length + 1)]
    ratio = sum(probabilities)
    probs = [x / ratio for x in probabilities]

    return probs


def plot_probabilities(length: int) -> None:
    """
    Plot probabilities.

    Used for debugging and visualising.
    """
    from matplotlib import pyplot

    probabilities = get_probabilities(length)
    pyplot.plot(range(1, length + 1), probabilities)
    pyplot.show()


def choose_card(cards: Sequence[Card]) -> Card:
    """Choose a card, weighted with the first cards more likely."""

    probabilities = get_probabilities(len(cards))

    choice = numpy.random.choice(cards, p=probabilities)
    assert isinstance(choice, Card)
    return choice


def print_card(card: Card) -> None:
    """Print a card to output."""

    print("=" * 16)
    print_safe(card.name)

    print("~" * 16)
    print_safe(card.desc)

    attachments = card.attachments
    if attachments:
        print("~" * 16)
        print("Attachments:")
        for attachment in attachments:
            print(attachment.url)

    print("~" * 16)
    print("Card:")
    print_safe(card.short_url)

    print("=" * 16)

    print("\n")


def get_action_from_user() -> Action:
    """Get action from user input."""
    action: Optional[Action] = None

    while action is None:
        prompt = ", ".join(action.description for action in ACTIONS[:-1])
        prompt += " or {}".format(ACTIONS[-1].description)
        prompt += ":\n"

        key = input(prompt)
        key = key.strip().lower()

        try:
            action = next(action for action in ACTIONS if action.key == key)
        except StopIteration:
            print("U wot m8?")

    return action


def print_card_stats(cards: Sequence[Card], card: Card) -> None:
    """Print card index and probability."""

    card_count = len(cards)
    card_index = cards.index(card)
    all_probs = get_probabilities(card_count)
    card_prob = all_probs[card_index]
    card_percent = card_prob * 100

    print("{:4d}/{:4d}, {:3.2f}%".format(card_index, card_count, card_percent))


def interactive(buy: bool = False, reverse: bool = False) -> None:
    """Fetch cards, show to user, get action, perform action."""
    while True:
        cards = get_cards(buy)
        if reverse:
            cards.reverse()
        card = choose_card(cards)

        print_card_stats(cards, card)

        try:
            print_card(card)
        except UnicodeEncodeError:
            print("Error printing card", card.short_url)
            exit()

        card_url = "https://api.trello.com/1/cards/{}?key={}&token={}".format(
            card.id, KEY, TOKEN
        )

        action = get_action_from_user()
        print(action.description)
        sys.stdout.flush()

        trello_action = action.trello_action
        if trello_action:
            requests.put(card_url, json=trello_action.request_data)
        elif action.key == "q":
            exit()

        print("\n" * 16)


def main() -> None:
    """Handle running as a script."""
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument("--plot", type=int)
    parser.add_argument("--buy", action="store_true")
    parser.add_argument("--reverse", action="store_true")

    args = parser.parse_args()
    if args.plot:
        plot_probabilities(args.plot)
    else:
        interactive(buy=args.buy, reverse=args.reverse)


if __name__ == "__main__":
    main()
