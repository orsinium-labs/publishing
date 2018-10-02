# Publishing

Trigger ifttt events with text from trello card when due date is reached.

Features:
1. Read cards from Trello.
1. Get any fields.
1. Drop cards after it (if you want)
1. Convert Markdown to HTML.
1. Convert Markdown to Telegram compatible HTML.
1. Multiple rules and Trello accounts support.


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
python3 -m publish
```
