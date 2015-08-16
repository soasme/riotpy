# -*- coding: utf-8 -*-

from riot.tags.tags import parse_tag_from_string
from riot.tags.style import parse_style
from riot.app import run_tag, quit_app

run_tag(
    parse_tag_from_string(
        '''
        <filler class="bg">
          <text class="streak" align="center">
            <span class="banner">hello world</span>
          </text>
        </filler>
        '''
    ), parse_style(
        '''
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
    ),
    unhandled_input=lambda key: key in ('q', 'Q') and quit_app()
)
