# -*- coding: utf-8 -*-

from pyquery import PyQuery
from urwid import ListBox, SimpleListWalker

def parse_tag_from_node(node):
    from .tags import parse_tag_from_node
    body = [parse_tag_from_node(PyQuery(child)) for child in node.children()]
    walker = SimpleListWalker(body)
    return ListBox(walker)
