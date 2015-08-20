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

def walk(root, fn):
    if not root:
        return
    if not fn(root):
        return
    for child in root.children().items():
        walk(child, fn)

def parse_expressions(root, dom, expressions):
    pass

def update_dom_opts(dom):
    return {}

def new_dom(impl, root, opts, inner_html):
    tag = Observable()
    tag.uuid = uuid4()
    tag.impl = impl
    tag.root = root
    tag.opts = opts or {} # FIXME: copy from opts.
    return tag

def mount_dom(root, dom):
    opts = update_dom_opts(dom)
    dom.impl.get('fn', lambda *a, **kwargs: None)(dom, opts)
    # parse expresions
    # mount child dom
    inner = dom.impl.get('html')
    root.html(inner)
    dom.is_mounted = True
    dom.trigger('mount')

def update_dom(dom):
    pass

def unmount_dom(dom):
    pass

def mixin_dom(dom):
    pass

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
        update_dom(dom)
