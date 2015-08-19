# -*- coding: utf-8 -*-

from functools import partial
from uuid import uuid4
from pyquery import PyQuery
from .observable import Observable

TAGS = {}
VDOM = {}

def define_tag(name, html, fn):
    TAGS[name] = dict(
        name=name,
        html=html,
        fn=fn
    )
    return TAGS[name]

def get_tag(name):
    return TAGS[name]

def new_dom(impl, root, opts, inner_html):
    tag = Observable()
    tag.uuid = uuid4()
    tag.impl = impl
    tag.conf = {
        'root': root,
        'opts': opts
    }
    return tag

def mount_dom(root, dom):
    root.html(dom.impl)

def pop_html(root):
    inner_html = root.html() or ''
    root.html('')
    return inner_html

def cache_dom(dom):
    VDOM[dom.uuid] = dom
    callback = lambda: expire_dom(dom.uuid)
    dom.on('unmounted', callback)

def get_dom(uuid):
    return VDOM[uuid]

def expire_dom(uuid):
    del VDOM[uuid]

def mount_tag(root, tag, opts):
    dom = new_dom(tag, root, opts, pop_html(root))
    mount_dom(root, dom)
    cache_dom(dom)
    return dom

def mount(root, selector, tagname='', opts=None):
    elements = root(selector)
    tags = []
    for element in elements:
        node = PyQuery(element)
        tagname = tagname or element.name
        node.__riot_tag__ = tagname
        tag = get_tag(tagname)
        dom = mount_to(node, tag, opts or {})
        tags.append(dom)
    return tags

def update():
    for tag in VDOM:
        tag.update()
