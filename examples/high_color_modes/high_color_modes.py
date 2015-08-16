# -*- coding: utf-8 -*-

import urwid

from riot.tags.style import parse_style
from riot.tags.utils import convert_string_to_node
from riot.tags.tags import parse_tag_from_node, riot_mount
from riot.app import quit_app, run_tag

style = '''
.banner {
  foreground-high: #ffa;
  background-high: #60d;
}
.streak {
  foreground-high: g50;
  background-high: #50a;
}
.inside {
  foreground-high: g38;
  background-high: #808;
}
.outside {
  foreground-high: g27;
  background-high: #a06;
}
.bg {
  foreground-high: g7;
  background-high: #d06;
}
'''

custom = '''
<custom>
  <filler class="bg">
    <pile>
      <div class="outside"></div>
      <div class="inside"></div>
      <text align="center" class="streak">
        <span class="banner">hello world</span>
      </text>
      <div class="inside"></div>
      <div class="outside"></div>
    </pile>
  </filler>
</custom>
'''

tag = '''
<solidfill class="bg"></solidfill>
'''

run_tag(
    parse_tag_from_node(
        riot_mount(
            convert_string_to_node(tag),
            'solidfill.bg',
            convert_string_to_node(custom)
        )
    ),
    parse_style(style),
    unhandled_input=lambda key: key in ('Q', 'q') and quit_app()
)
