import re
from markdown2 import markdown
from .markdown import Parser


converters = dict(
    html=markdown,
    telegram_html=Parser(),
    dash=lambda text: text.replace(' -- ', ' — '),
    links=lambda text: re.sub(
        r'(\w) \((https.*?)\)',
        r'[\1](\2)',
        text,
    ),
)
