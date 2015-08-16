# -*- coding: utf-8 -*-

from urwid import Divider

def parse_tag_from_node(node):
    div_char = node.attr.div_char or u' '
    top = int(node.attr.top or 0)
    bottom = int(node.attr.bottom or 0)
    return Divider(div_char=div_char, top=top, bottom=bottom)
