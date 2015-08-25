# -*- coding: utf-8 -*-

from urwid import Button

def parse_tag_from_node(node):
    label = node.attr.label or u'click'
    return Button(label=label)
