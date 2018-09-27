from .trello import Trello
from .config import load
from .ifttt import IFTTT


def publish():
    config = load()

    trello_connections = dict()
    for name, credentials in config['connections'].items():
        trello_connections[name] = Trello(credentials)

    for rule in config['rules']:
        trello = trello_connections[rule['connection']]
        ifttt = IFTTT(key=config['ifttt']['key'], rule=rule)
        for card in trello.get_posts(rule):
            print(card.name)
            ifttt.send(card)
