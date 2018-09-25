from datetime import datetime, timezone

import tomlkit
import requests
from markdown2 import markdown
from trello import TrelloClient


CONFIG_PATH = './config.toml'
with open(CONFIG_PATH) as stream:
    config = tomlkit.parse(stream.read())


class Trello:
    def __init__(self, config):
        self.board_name = config['board']
        self.list_name = config['list']
        self.board_id = config.get('board_id')
        self.list_id = config.get('list_id')

        self.client = TrelloClient(
            api_key=config['key'],
            # api_secret=,
            token=config['token'],
            token_secret=config['oauth_secret'],
        )

    def get_board(self):
        if self.board_id:
            return self.client.get_board(self.board_id)

        boards = self.client.list_boards()
        choosen = []
        for board in boards:
            if board.name == self.board_name:
                choosen.append(board)

        if len(choosen) == 0:
            raise KeyError('Board {} not found. Available: {}'.format(
                self.board_name,
                ','.join(board.name for board in boards),
            ))

        if len(choosen) == 1:
            self.board_id = choosen[0].id
            return choosen[0]

        if len(choosen) > 1:
            raise ValueError('Found {count} boards with name {name}'.format(
                count=len(choosen),
                name=self.board_name,
            ))

    def get_list(self, board):
        if self.list_id:
            return board.get_list(self.list_id)

        lists = board.list_lists()
        choosen = []
        for lst in lists:
            if lst.name == self.list_name:
                choosen.append(lst)

        if len(choosen) == 0:
            raise KeyError('List {} not found. Available: {}'.format(
                self.list_name,
                ','.join(lst.name for lst in lists),
            ))

        if len(choosen) == 1:
            self.list_id = choosen[0].id
            return choosen[0]

        if len(choosen) > 1:
            raise ValueError('Found {count} lists with name {name}'.format(
                count=len(choosen),
                name=self.list_name,
            ))

    def save(self, config):
        if 'board' in config:
            del config['board']
        config['board_id'] = self.board_id
        config['board_id'].comment(self.board_name)

        if 'list' in config:
            del config['list']
        config['list_id'] = self.list_id
        config['list_id'].comment(self.list_name)

    def get_posts(self):
        board = self.get_board()
        lst = self.get_list(board)
        now = datetime.now(timezone.utc)
        for card in lst.list_cards():
            if card.due_date and card.due_date <= now:
                yield card
                card.delete()


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


if __name__ == '__main__':
    publish()
