from markdown2 import markdown


converters = dict(
    html=markdown,
    dash=lambda text: text.replace(' -- ', ' — '),
    links=...,
)
