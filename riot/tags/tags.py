# -*- coding: utf-8 -*-

import re
import uuid

from pyquery import PyQuery

from . import text, filler, div, pile, solidfill, edit
from .utils import convert_string_to_node, detect_class

convert_to_node = convert_string_to_node

def parse_tag_from_string(string):
    return parse_tag_from_node(convert_string_to_node(string))

def set_riot_attr(node, key, value):
    node.attr['__riot_%s__' % key] == str(value)

def get_riot_attr(node, key):
    return node.attr['__riot_%s__' % key]

@detect_class
def parse_tag_from_node(node):
    tagname = node[0].tag
    is_mounted = get_riot_attr(node, 'is_mounted') == 'true'
    if is_mounted:
        return parse_tag_from_node(convert_to_node(node.children()))
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

def riot_mount(dom, selector, node, mount_args={}):
    pq = dom(selector)
    set_riot_attr(pq, 'is_mounted', 'true')
    pq.html(node.html())
    return dom
