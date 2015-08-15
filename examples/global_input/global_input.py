# -*- coding: utf-8 -*-

from riot.tags.tags import parse_tag_from_string
from riot.app import run_tag, quit_app

tag = parse_tag_from_string(
    '''
    <filler valign="top">
      <text>Hello World</text>
    </filler>
    '''
)

def show_or_exit(key):
    if key in ('Q', 'q'):
        quit_app()
    tag.body.set_text(repr(key))

run_tag(tag, unhandled_input=show_or_exit)
