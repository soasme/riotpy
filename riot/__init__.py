# -*- coding: utf-8 -*-

import urwid

def parse_tagfile(tagfile):
    with open(tagfile, 'rb') as tagfile_obj:
        parse_tag_expressions(tagfile_obj.read())

def riot_open(tagfile, *args, **kwargs):
    custom_tags, layout = parse_tagfile(tagfile)
    app = render_layout(custom, layout, *args, **kwargs)
    loop = urwid.MainLoop(app)
    loop.run()
