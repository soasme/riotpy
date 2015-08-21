# -*- coding: utf-8 -*-

from functools import partial
from uuid import uuid4
from pyquery import PyQuery
from .virtual_node import new_node
from .observable import Observable
from .utils import (
    walk, # walk tree
)

TAGS = {} # place custom tag definition, with {?tagname: {name:, html:, fn:, }}
VDOM = {} # place Virtual DOMs, with {?uuid: tag_instance }

def pop_html(root):
    inner_html = root.html() or ''
    root.html('')
    return inner_html

def define_tag(name, html, fn):
    TAGS[name] = dict(
        name=name,
        html=html,
        fn=fn
    )
    return TAGS[name]

def is_tag_defined(name):
    return name in TAGS

def get_tag(name):
    return TAGS[name]

def cache_dom(dom):
    VDOM[dom.uuid] = dom
    callback = lambda: expire_dom(dom.uuid)
    dom.on('unmounted', callback)

def get_dom(uuid):
    return VDOM[uuid]

def expire_dom(uuid):
    del VDOM[uuid]

def mount_tag(root, tag, opts):
    node = new_node(tag, root, opts, pop_html(root))
    node.mount()
    cache_dom(node)
    return node

def mount(root, selector, tagname='', opts=None):
    elements = root(selector)
    doms = []
    for element in elements:
        node = PyQuery(element)
        tagname = tagname or element.name
        node.__riot_tag__ = tagname
        tag = get_tag(tagname)
        dom = mount_tag(node, tag, opts or {})
        doms.append(dom)
    return doms

def update():
    for dom in VDOM:
        dom.update({})
