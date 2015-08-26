# -*- coding: utf-8 -*-

from urwid import Edit

def parse_tag_from_node(node):
    caption = node.attr.caption  or u''
    return Edit(caption=caption)

META = {
    'attribute_methods': {
    }
}
