# -*- coding: utf-8 -*-

from uuid import uuid4
from pyquery import PyQuery
from .observable import Observable

TAG_IMPL = {}
VDOM = {}

def new_tag(impl, root, opts, inner_html):
    tag = Observable()
    tag.uuid = uuid4()
    tag.impl = impl
    tag.conf = {
        'root': root,
        'opts': opts
    }
    return tag

def pop_html(root):
    inner_html = root.html() or ''
    root.html('')
    return inner_html

def mount_tag(tag):
    pass

def mount_to(root, layout, opts):
    tag = new_tag(layout, root, opts, pop_html(root))
    mount_tag(tag)
    VDOM[tag.uuid] = tag
    tag.on('unmounted', lambda: VDOM.__delitem__(tag.uuid)) # del VDOM[tag.uuid]
    return tag

def register_layout(name, html, fn):
    TAG_IMPL[name] = dict(
        name=name,
        html=html,
        fn=fn,
    )
    return name

def get_layout(name):
    return TAG_IMPL[name]

def mount(root, selector, tagname='', opts=None):
    elements = root(selector)
    tags = []
    for element in elements:
        node = PyQuery(element)
        tagname = tagname or element.name
        node.__riot_tag__ = tagname
        layout = get_layout(tagname)
        tag = mount_to(node, layout, opts or {})
        tags.append(tag)
    return tags
