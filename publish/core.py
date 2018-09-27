from .trello import Trello
from .config import load, dump
from .ifttt import IFTTT


def publish(path=None):
    config = load(path)

    trello_connections = dict()
    for name, credentials in config['connections'].items():
        trello_connections[name] = Trello(credentials)

    for rule in config['rules']:
        trello = trello_connections[rule['connection']]
        ifttt = IFTTT(key=config['ifttt']['key'], rule=rule)
        for card in trello.get_posts(rule):
            print(card.name)
            ifttt.send(card)

    dump(config=config, path=path)
