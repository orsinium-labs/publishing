# Publishing

Trigger ifttt events with text from trello card when due date is reached.

Features:
1. Convert Markdown to HTML.

## Installation

```bash
git clone https://github.com/orsinium/publishing.git
cd publishing
pip3 install --user -r requirements.txt
cp config{_example,}.toml
```

After that edit `config.toml`.

## Send cards to IFTTT

```bash
python3 publish.py
```
