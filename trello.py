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
    "k": {"description": "[K]eep"},
    "a": {"description": "[A]rchive", "data": {"closed": True}},
    "b": {"description": "[B]uy (later)", "data": {"idList": BUY_LIST}},
    "t": {"description": "Move to [t]op", "data": {"pos": "top"}},
    "q": {"description": "[Q]uit!"},
}


def print_safe(something):
    """Print a string after encoding / decoding to remove unsafe chars."""
    print(something.encode("ascii", "replace").decode("ascii"))


def get_cards(buy):
    """Fetch all cards from the trello list."""
    list_id = BUY_LIST if buy else LISTEN_LIST

    fields = ["id", "name", "desc", "shortUrl"]
    url = "https://api.trello.com/1/lists/{}/cards?fields={}&key={}&token={}".format(
        list_id, ",".join(fields), KEY, TOKEN
    )
    response = requests.get(url)
    cards = response.json()
    return cards


def get_probabilities(length):
    """Return probabilities for a given length."""
    probabilities = [x ** -1 for x in range(1, length + 1)]
    ratio = sum(probabilities)
    probs = [x / ratio for x in probabilities]
    return probs


def plot_probabilities(length):
    """
    Plot probabilities.

    Used for debugging and visualising.
    """
    from matplotlib import pyplot

    probabilities = get_probabilities(length)
    pyplot.plot(range(1, length + 1), probabilities)
    pyplot.show()


def choose_card(cards):
    """Choose a card, weighted with the first cards more likely."""
    probabilities = get_probabilities(len(cards))
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


def print_card_stats(cards, card):
    """Print card index and probability."""

    card_count = len(cards)
    card_index = cards.index(card)
    all_probs = get_probabilities(card_count)
    card_prob = all_probs[card_index]
    card_percent = card_prob * 100

    print("{:4d}/{:4d}, {:3.2f}%".format(card_index, card_count, card_percent))


def interactive(buy=False, reverse=False):
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
            print("Error printing card", card["shortUrl"])
            exit()

        card_url = "https://api.trello.com/1/cards/{}?key={}&token={}".format(
            card["id"], KEY, TOKEN
        )

        action = get_action_from_user()
        print(ACTIONS[action]["description"])
        sys.stdout.flush()

        data = ACTIONS[action].get("data")
        if data:
            requests.put(card_url, json=data)
        elif action == "q":
            exit()

        print("\n" * 16)


def main():
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
