# -*- coding: utf-8 -*-

import re
from uuid import uuid4, UUID
from pyquery import PyQuery

from . import text, filler, div, pile, solidfill, edit, button
from ..observable import Observable
from ..virtual_dom import get_dom
from .utils import convert_string_to_node, detect_class

convert_to_node = convert_string_to_node

def parse_tag_from_string(string):
    return parse_tag_from_node(convert_string_to_node(string))

@detect_class
def parse_tag_from_node(node):
    tagname = node[0].tag
    uuid = node.attr.__riot_uuid__
    if uuid:
        ui = get_dom(UUID(uuid)).ui
    elif tagname == 'text':
        ui = text.parse_tag_from_node(node)
    elif tagname == 'filler':
        ui = filler.parse_tag_from_node(node)
    elif tagname == 'div':
        ui = div.parse_tag_from_node(node)
    elif tagname == 'pile':
        ui = pile.parse_tag_from_node(node)
    elif tagname == 'solidfill':
        ui = solidfill.parse_tag_from_node(node)
    elif tagname == 'edit':
        ui = edit.parse_tag_from_node(node)
    elif tagname == 'button':
        ui = button.parse_tag_from_node(node)
    else:
        raise NotImplementedError(tagname)

    return ui
