from publish.markdown import Parser


telegram_html = Parser()


def test_a():
    md = '[text](https://link.com) me'
    html = '<a href="https://link.com">text</a> me'
    assert telegram_html(md) == html


def test_br():
    md = 'text\nme'
    html = 'text<br/>\nme'
    assert telegram_html(md) == html


def test_i():
    md = '*text* me'
    html = '<i>text</i> me'
    assert telegram_html(md) == html

    md = 'do not _text_ me'
    html = 'do not <i>text</i> me'
    assert telegram_html(md) == html


def test_b():
    md = '**text** me'
    html = '<b>text</b> me'
    assert telegram_html(md) == html

    md = '__text__ me'
    html = '<b>text</b> me'
    assert telegram_html(md) == html


def test_pre():
    md = 'never\n ```\ngonna __give__\n```\nyou up'
    html = 'never<br/>\n <pre>gonna __give__</pre>\n<br/>\nyou up'
    assert telegram_html(md) == html

    md = '__text__ me'
    html = '<b>text</b> me'
    assert telegram_html(md) == html


def test_code():
    md = 'never `gonna __give__` you up'
    html = 'never <code>gonna __give__</code> you up'
    assert telegram_html(md) == html

    md = '__text__ me'
    html = '<b>text</b> me'
    assert telegram_html(md) == html


def test_couple():
    md = 'never *gonna* **give** _you_ __up__'
    html = 'never <i>gonna</i> <b>give</b> <i>you</i> <b>up</b>'
    assert telegram_html(md) == html

    md = '[never](gonna)\n[give](you)'
    html = '<a href="gonna">never</a><br/>\n<a href="you">give</a>'
    assert telegram_html(md) == html
