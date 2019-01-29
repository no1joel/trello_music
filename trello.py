"""Return a random trello from the stuff to check out list that I have."""

import sys

import numpy
import requests

import settings

KEY = settings.KEY
TOKEN = settings.TOKEN
LISTEN_LIST = settings.LISTEN_LIST
BUY_LIST = settings.BUY_LIST


ACTIONS = {
    "k": {"description": "[K]eep", "data": None},
    "a": {"description": "[A]rchive", "data": {"closed": True}},
    "b": {"description": "[B]uy (later)", "data": {"idList": BUY_LIST}},
    "t": {"description": "Move to [t]op", "data": {"pos": "top"}},
}


def print_safe(something):
    """Print a string after encoding / decoding to remove unsafe chars."""
    print(something.encode("utf-8", "replace").decode("utf-8"))


def get_cards():
    """Fetch all cards from the trello list."""
    fields = ["id", "name", "desc", "shortUrl"]
    url = "https://api.trello.com/1/lists/{}/cards?fields={}&key={}&token={}".format(
        LISTEN_LIST, ",".join(fields), KEY, TOKEN
    )
    response = requests.get(url)
    cards = response.json()
    return cards


def choose_card(cards):
    """Choose a card, weighted with the first cards more likely."""
    probabilities = (1 / x for x in range(len(cards)))
    return numpy.random.choice(cards, p=probabilities)


def print_card(card):
    """Print a card to output."""
    print("=" * 16)
    print_safe(card["name"])
    print("~" * 16)
    print_safe(card["desc"])
    print("~" * 16)
    print_safe(card["shortUrl"])
    print("=" * 16)

    print("\n")


def get_action_from_user():
    """Get action from user input."""
    action = ""

    while action not in ACTIONS:
        keys = list(ACTIONS.keys())
        prompt = ", ".join(ACTIONS[k]["description"] for k in keys[:-1])
        prompt += " or {}".format(ACTIONS[keys[-1]]["description"])
        prompt += ":\n"
        action = input(prompt)
        action = action.strip().lower()
        if action not in ACTIONS:
            print("U wot m8?")

    return action


def main():
    """Fetch cards, show to user, get action, perform action."""
    while True:
        cards = get_cards()
        card = choose_card(cards)
        print_card(card)

        card_url = "https://api.trello.com/1/cards/{}?key={}&token={}".format(
            card["id"], KEY, TOKEN
        )

        action = get_action_from_user()
        print(ACTIONS[action]["description"])
        sys.stdout.flush()

        data = ACTIONS[action]["data"]
        if data:
            requests.put(card_url, json=data)

        print("\n" * 16)


if __name__ == "__main__":
    main()
