import requests
import random
import sys
import settings


KEY = settings.KEY
TOKEN = settings.TOKEN
LISTEN_LIST = settings.LISTEN_LIST
BUY_LIST = settings.BUY_LIST


fields = ["id", "name", "desc" , "shortUrl"]
url = (
    "https://api.trello.com/1/lists/{}/cards"
    "?fields={}&key={}&token={}".format(LISTEN_LIST, ",".join(fields), KEY, TOKEN)
)

while True:
    response = requests.get(url)
    cards = response.json()
    weighted_cards = []
    for index, card in enumerate(cards):
        weight = len(cards) - index
        for w in range(weight):
            weighted_cards.append(card)
    card = random.choice(weighted_cards)

    print("=" * 16)
    print(card["name"])
    print("~" * 16)
    print(card["desc"])
    print("~" * 16)
    print(card["shortUrl"])
    print("=" * 16)

    print("\n")

    actions = {
        "k": {
            "description": "[K]eep",
            "data": None
        },
        "a": {
            "description": "[A]rchive",
            "data": {"closed": True},
        },
        "b": {
            "description": "[B]uy (later)",
            "data": {"idList": BUY_LIST},
        },
        "t": {
            "description": "Move to [t]op",
            "data": {"pos": "top"}
        }
    }

    action = ""

    while action not in actions:
        keys = list(actions.keys())
        prompt = ", ".join(actions[k]["description"] for k in keys[:-1])
        prompt += " or {}".format(actions[keys[-1]]["description"])
        prompt += ":\n"
        action = input(prompt)
        action = action.strip().lower()
        if action not in actions:
            print("U wot m8?")

    card_url = "https://api.trello.com/1/cards/{}?key={}&token={}".format(
        card["id"], KEY, TOKEN
    )

    print(actions[action]["description"])
    sys.stdout.flush()

    data = actions[action]["data"]
    response = requests.put(card_url, json=data)
    print("\n" * 16)
