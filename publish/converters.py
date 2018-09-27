import re
from markdown2 import markdown


converters = dict(
    html=markdown,
    dash=lambda text: text.replace(' -- ', ' — '),
    links=lambda text: re.sub(
        r'(\w) \((https.*?)\)',
        r'[\1](\2)',
        text,
    ),
)
