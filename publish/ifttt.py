import requests
from .converters import converters


class IFTTT:
    url_template = 'https://maker.ifttt.com/trigger/{event}/with/key/{key}'

    def __init__(self, key, rule):
        self.url = self.url_template.format(
            event=rule['event'],
            key=key,
        )
        self.rule = rule

    def convert(self, text):
        for converter_name in self.rule['converters']:
            text = converters[converter_name](text)
        return text

    def make_request(self, card):
        mapping = dict(
            description=self.convert(card.description),
            name=card.name,
            due_date=card.due_date.isoformat(),
        )

        request = dict()
        for number, field in enumerate(self.rule['fields'], start=1):
            request['value' + str(number)] = mapping[field]
        return request

    def send(self, card):
        print(card.name)
        requests.post(self.url, json=self.make_request(card))
