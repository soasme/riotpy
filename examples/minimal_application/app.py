# -*- coding: utf-8 -*-

from riot.tags.tags import parse_tag_from_string
from riot.app import run_tag

run_tag(
    parse_tag_from_string(
        '''
        <filler valign="top">
          <text>hello world!</text>
        </filler>
        '''
    )
)
