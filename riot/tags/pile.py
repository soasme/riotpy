# -*- coding: utf-8 -*-

from pyquery import PyQuery
from urwid import Pile

def parse_tag_from_node(node):
    from . import tags
    children = [tags.parse_tag_from_node(PyQuery(child)) for child in node.children()]
    return Pile(children)
