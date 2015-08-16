# -*- coding: utf-8 -*-

from riot.tags.tags import parse_tag_from_string
from riot.tags.style import parse_style
from riot.app import run_tag, quit_app

def exit_on_q(key):
    if key in ('q', 'Q'):
        quit_app()

string = '''
<filler class="bg">
  <text class="streak" align="center">
    <span class="banner">Hello World</span>
  </text>
</filler>
'''

style = '''
.banner {
  foreground: black;
  background: light gray;
}
.streak {
  foreground: black;
  background: dark red;
}
.bg {
  foreground: black;
  background: dark blue;
}
'''

run_tag(
    parse_tag_from_string(string), parse_style(style),
    unhandled_input=exit_on_q
)
