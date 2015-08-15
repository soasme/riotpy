# -*- coding: utf-8 -*-

import urwid
from riot.tags.tags import parse_tag_from_string

fill = parse_tag_from_string('<filler valign="top"><text>hello world!</text></filler>')
loop = urwid.MainLoop(fill)
loop.run()
