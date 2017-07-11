import base64
from collections import deque, namedtuple
from html.entities import name2codepoint
from html.parser import HTMLParser

# Point = namedtuple('Point',['x','y'])

# p = Point(1,2)

# print(p.x,p.y)

# q = deque(['a','b','c'])
# q.append('x')
# q.appendleft('y')
# print(q)

# s = base64.b64encode(b'binary\x00string')
# s1 = base64.urlsafe_b64encode(b'i\xb7\x1d\xfb\xef\xff')
# print(s)
# print(s1)


class MyHTMLParser(HTMLParser):

    def handle_starttag(self, tag, attrs):
        print('<%s>' % tag)

    def handle_endtag(self, tag):
        print('</%s>' % tag)

    def handle_startendtag(self, tag, attrs):
        print('<%s/>' % tag)

    def handle_data(self, data):
        print(data)

    def handle_comment(self, data):
        print('<!--', data, '-->')

    def handle_entityref(self, name):
        print('&%s;' % name)

    def handle_charref(self, name):
        print('&#%s;' % name)

parser = MyHTMLParser()
parser.feed('''<html>
<head></head>
<body>
<!-- test html parser -->
    <p>Some <a href=\"#\">html</a> HTML&nbsp;tutorial...<br>END</p>
</body></html>''')
