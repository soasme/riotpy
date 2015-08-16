# -*- coding: utf-8 -*-

from riot.tags.tags import parse_tag_from_string
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

import urwid

palette = [
    ('banner', 'black', 'light gray'),
    ('streak', 'black', 'dark red'),
    ('bg', 'black', 'dark blue'),]

map3 = parse_tag_from_string(string)
loop = urwid.MainLoop(map3, palette, unhandled_input=exit_on_q)
loop.run()
