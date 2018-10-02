from collections import OrderedDict, namedtuple
import re


Token = namedtuple('Token', ['name', 'match'])


# trello:
# https://help.trello.com/article/821-using-markdown-in-trello
# telegram:
# https://core.telegram.org/bots/api#html-style

class Parser:
    # https://github.com/lepture/mistune/blob/583d358296bb10c0f66ba643e9ee574e8af96db0/mistune.py#L464
    parsers = OrderedDict((
        ('pre', re.compile(r'\`{3}([\s\S]+?)\`{3}')),
        ('a', re.compile(
            r'!?\[('
            r'(?:\[[^^\]]*\]|[^\[\]]|\](?=[^\[]*\]))*'
            r')\]\('
            r'''\s*(<)?([\s\S]*?)(?(2)>)(?:\s+['"]([\s\S]*?)['"])?\s*'''
            r'\)'
        )),
        ('b', re.compile(
            r'_{2}([\s\S]+?)_{2}(?!_)'  # __word__
            r'|'
            r'\*{2}([\s\S]+?)\*{2}(?!\*)'  # **word**
        )),
        ('i', re.compile(
            r'\b_((?:__|[^_])+?)_\b'  # _word_
            r'|'
            r'\*((?:\*\*|[^\*])+?)\*(?!\*)'  # *word*
        )),
        ('br', re.compile(r' {2,}\n(?!\s*$)')),
    ))

    subs = dict(
        b=r'<b>\1\2</b>',
        i=r'<i>\1\2</i>',
        a=r'<a href="\3">\1</a>',
        br=r'\1<br/>',
        pre=r'<pre>\1</pre>',
    )

    placeholder = '§'

    def __call__(self, text):
        tokens = []
        for name, parser in self.parsers.items():
            for match in parser.finditer(text):
                tokens.append(Token(name=name, match=match))
                text = self.extract_match(match=match, text=text)
        for token in tokens:
            text = self.insert_sub(match=token.match, text=text, sub=self.subs[token.name])
        return text

    def extract_match(self, match, text):
        before = text[:match.start()]
        after = text[match.end():]
        holder = self.placeholder * (match.end() - match.start())
        return before + holder + after

    @staticmethod
    def insert_sub(match, text, sub):
        before = text[:match.start()]
        after = text[match.end():]
        holder = match.expand(sub)
        return before + holder + after