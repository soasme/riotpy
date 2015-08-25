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
            rs.append(_node)
        elif _node.tag == 'span':
            if_ = _node.get('if', 'True')
            if if_ == '':
                continue
            class_name = _node.get('class', '')
            span_markup = parse_markup(_node)
            markup = (class_name, span_markup) if class_name else span_markup
            rs.append(markup)
    if len(rs) == 1 and isinstance(rs[0], basestring):
        return rs[0]
    if not rs:
        return ''
    return rs

def parse_tag_from_node(node):
    align = node.attr.align or 'left'
    wrap = node.attr.wrap or 'space'
    if len(node.children()) == 0:
        markup = node.text()
    else:
        markup = parse_markup(node)
    return Text(markup=markup, align=align, wrap=wrap)

META = {
    'attribute_methods': {
        'inner_html': 'set_text',
    }
}
