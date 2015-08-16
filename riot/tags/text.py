# -*- coding: utf-8 -*-

from urwid import Text
from pyquery import PyQuery

from .utils import convert_string_to_node


def parse_tag_from_string(string):
    return parse_tag_from_node(convert_string_to_node(string))

def parse_markup(node):
    rs = []
    for _node in PyQuery(node).contents():
        if isinstance(_node, str):
            rs.append(_node.strip())
        elif _node.tag == 'span':
            class_name = _node.get('class', '')
            span_markup = parse_markup(_node)
            markup = (class_name, span_markup) if class_name else span_markup
            rs.append(markup)
    return rs

def parse_tag_from_node(node):
    align = node.attr.align or 'left'
    wrap = node.attr.wrap or 'space'
    if len(node.children()) == 0:
        markup = node.text()
    else:
        markup = parse_markup(node)
    return Text(markup=markup, align=align, wrap=wrap)
