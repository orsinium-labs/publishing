from publish.markdown import Parser


telegram_html = Parser()


def test_a():
    md = '[text](https://link.com) me'
    html = '<a href="https://link.com">text</a> me'
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
    md = """
    never
    ```
    gonna
    __give__
    ```
    you up
    """
    html = """
    never
    <pre>
    gonna
    __give__
    </pre>
    you up
    """
    assert telegram_html(md) == html

    md = '__text__ me'
    html = '<b>text</b> me'
    assert telegram_html(md) == html
