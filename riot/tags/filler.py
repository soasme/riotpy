# -*- coding: utf-8 -*-

from pyquery import PyQuery
from urwid import Filler

def parse_tag_from_node(node):
    from . import tags
    valign = node.attr.valign or 'middle'
    children = node.children()
    assert len(children) == 1, 'Filler can only have one child.'
    filler = Filler(tags.parse_tag_from_node(PyQuery(children[0])), valign)
    return filler
