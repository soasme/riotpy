# -*- coding: utf-8 -*-

import urwid
import riot.tags.text as text

txt = text.parse_tag_from_string('<text>Hello World</text>')
fill = urwid.Filler(txt, 'top')
loop = urwid.MainLoop(fill)
loop.run()
