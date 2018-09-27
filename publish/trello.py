from datetime import datetime, timezone
from trello import TrelloClient


class Trello:
    def __init__(self, config):
        self.client = self.get_connection(config)

    @staticmethod
    def get_connection(config):
        return TrelloClient(
            api_key=config['key'],
            token=config['token'],
            token_secret=config['oauth_secret'],
        )

    def get_board(self, *, board_name=None, board_id=None):
        if board_id:
            return self.client.get_board(board_id)

        boards = self.client.list_boards()
        choosen = []
        for board in boards:
            if board.name == board_name:
                choosen.append(board)

        if len(choosen) == 0:
            raise KeyError('Board {} not found. Available: {}'.format(
                board_name,
                ','.join(board.name for board in boards),
            ))

        if len(choosen) == 1:
            return choosen[0]

        if len(choosen) > 1:
            raise ValueError('Found {count} boards with name {name}'.format(
                count=len(choosen),
                name=board_name,
            ))

    def get_list(self, board, *, list_id=None, list_name=None):
        if list_id:
            return board.get_list(list_id)

        lists = board.list_lists()
        choosen = []
        for lst in lists:
            if lst.name == list_name:
                choosen.append(lst)

        if len(choosen) == 0:
            raise KeyError('List {} not found. Available: {}'.format(
                list_name,
                ','.join(lst.name for lst in lists),
            ))

        if len(choosen) == 1:
            return choosen[0]

        if len(choosen) > 1:
            raise ValueError('Found {count} lists with name {name}'.format(
                count=len(choosen),
                name=list_name,
            ))

    @staticmethod
    def save(rule, *, board_id=None, list_id=None, board_name=None, list_name=None):
        if 'board' in rule:
            del rule['board']
        if board_name and board_id:
            rule['board_id'] = board_id
            rule['board_id'].comment(board_name)

        if 'list' in rule:
            del rule['list']
        if list_name and list_id:
            rule['list_id'] = list_id
            rule['list_id'].comment(list_name)

    def get_posts(self, rule):
        board = self.get_board(
            board_name=rule.get('board'),
            board_id=rule.get('board_id'),
        )
        lst = self.get_list(
            board=board,
            list_name=rule.get('list'),
            list_id=rule.get('list_id'),
            )

        now = datetime.now(timezone.utc)
        for card in lst.list_cards():
            if card.due_date and card.due_date <= now:
                yield card
                if rule['delete']:
                    card.delete()

        self.save(
            rule=rule,
            board_name=board.name,
            board_id=board.id,
            list_name=lst.name,
            list_id=lst.id,
        )
