# -*- coding: utf-8 -*-

import re
from uuid import uuid4
from pyquery import PyQuery

from . import text, filler, div, pile, solidfill, edit
from ..observable import Observable
from .utils import convert_string_to_node, detect_class

convert_to_node = convert_string_to_node

def parse_tag_from_string(string):
    return parse_tag_from_node(convert_string_to_node(string))

@detect_class
def parse_tag_from_node(node):
    tagname = node[0].tag
    is_mounted = node.attr.__riot_is_mounted__ == "true"
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
    pq.attr.__riot_is_mounted__ = 'true'
    pq.html(node.html())
    return dom

TAG_IMPL = {}
VDOM = {}
def mounte_to(root, tagname, opts):
    impl = TAG_IMPL.get(tagname)
    if not impl:
        return
    inner_html = root.html() or ''
    root.html('')
    tag = Observable()
    tag.uuid = uuid4()
    tag.impl = impl
    tag.conf = {
        'root': root,
        'opts': opts
    }
    @tag.on('unmounted')
    def on_tag_unmounted(tag):
        del VDOM[tag.uuid]

def define_tag(name, html, fn):
    TAG_IMPL[name] = dict(
        name=name,
        html=html,
        fn=fn,
    )
    return name

def mount(root, selector, tagname, opts):
    elements = root(selector)
    if not elements:
        return []
