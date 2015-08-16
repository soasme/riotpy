# -*- coding: utf-8 -*-

from . import text, filler
from .utils import convert_string_to_node, detect_class

def parse_tag_from_string(string):
    return parse_tag_from_node(convert_string_to_node(string))

@detect_class
def parse_tag_from_node(node):
    tagname = node[0].tag
    if tagname == 'text':
        return text.parse_tag_from_node(node)
    elif tagname == 'filler':
        return filler.parse_tag_from_node(node)
    else:
        raise NotImplementedError
