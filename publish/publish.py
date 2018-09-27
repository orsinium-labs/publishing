from .trello import Trello, get_connection
from .config import config
import requests


def publish():
    URL = 'https://maker.ifttt.com/trigger/{event}/with/key/{key}'.format(
        event=config['ifttt']['event'],
        key=config['ifttt']['key'],
    )
    trello = Trello(config['trello'])

    for card in trello.get_posts():
        print(card.name)
        post = markdown(card.description)  # convert md to html
        requests.post(URL, json=dict(value1=post))

    trello.save(config['trello'])
    with open(CONFIG_PATH, 'w') as stream:
        stream.write(tomlkit.dumps(config))
