# -*- coding: utf-8 -*-

import urwid

from riot.tags.tags import parse_tag_from_string
from riot.app import run_tag

run_tag(
    parse_tag_from_string(
        '''
        <filler valign="middle">
          <text>hello world!</text>
        </filler>
        '''
    )
)
