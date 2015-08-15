# -*- coding: utf-8 -*-

from urwid import Text

from .utils import convert_string_to_node


def parse_tag_from_string(string):
    return parse_tag_from_node(convert_string_to_node(string))

def parse_tag_from_node(node):
    align = node.attr.align or 'left'
    wrap = node.attr.wrap or 'space'
    markup = node.text()
    return Text(markup=markup, align=align, wrap=wrap)
