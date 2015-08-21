# -*- coding: utf-8 -*-

import re
from uuid import uuid4, UUID
from pyquery import PyQuery

from . import text, filler, div, pile, solidfill, edit
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
        return get_dom(UUID(uuid)).ui
    if tagname == 'text':
        return text.parse_tag_from_node(node)
    elif tagname == 'filler':
        return filler.parse_tag_from_node(node)
    elif tagname == 'div':
        return div.parse_tag_from_node(node)
    elif tagname == 'pile':
        return pile.parse_tag_from_node(node)
    elif tagname == 'solidfill':
        return solidfill.parse_tag_from_node(node)
    elif tagname == 'edit':
        return edit.parse_tag_from_node(node)
    else:
        raise NotImplementedError(tagname)

