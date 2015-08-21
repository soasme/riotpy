# -*- coding: utf-8 -*-

from uuid import uuid4
from .observable import Observable
from .expression import update_expressions, parse_expressions
from .template import render_template

def new_node(impl, inner, **kwargs):
    node = Observable()
    node.uuid = uuid4()
    node.impl = impl
    node.inner = inner
    node.children = []
    node.expressions = []
    node.opts = kwargs.get('opts') or {}
    node.root = kwargs.get('root')
    node.parent = kwargs.get('parent')
    node.dom = make_dom(node)
    node.update = lambda data: update_node(node, data)
    node.mount = lambda: mount_node(node)
    node.unmount = lambda: unmount_node(node)
    return node

def new_child_node(impl, dom, parent):
    node = new_node(impl, dom.html())
    return node

def mount_children_nodes(node):
    for child in node.children:
        mount_node(child)
    if node.parent:
        node.parent\
            .on('update', node.update)\
            .on('unmount', node.unmount)

def unmount_children_nodes(node):
    for child in node.children:
        unmount_node(child)
    if node.parent:
        node.parent\
            .off('update', node.update)\
            .off('unmount', node.unmount)

def unmount_node(node):
    root_parent = node.root.parent()
    root_parent.html('')
    node.trigger('unmount')
    unmount_children_nodes(node)
    node.off_all()

def clean_up_data(data):
    if not hasattr(data, 'trigger'):
        return data
    del data.trigger
    return data

def inherit_from_parent(node):
    pass

def normalize_data(data):
    return data

def render_opts(node):
    opts = {}
    for attribute, value in node[0].attrib.items():
        opts[attribute] = render_template(value, node)
    return opts

def extend_node(node, data):
    node.opts = render_opts(node)
    for key, value in data.items():
        setattr(self, key, value)

def update_node(node, data):
    inherit_from_parent(node)
    data = clean_up_data(data)
    data = normalize_data(data)
    extend_node(node, data)
    node.trigger('update', data)
    update_expressions(node.expressions, node)
    node.trigger('updated')

def make_dom(node):
    return PyQuery(node.impl.get('html'))

def mount_node(node):
    node.opts = render_opts(node)
    node.impl.get('fn')(node, node.opts)
    parse_expressions(node)
    mount_children_nodes(node)
    _ = node.root and parse_expressions(node.root, node, node.expressions)
    node.trigger('premount')
    dom = make_dom(node)

    if not node.parent or node.parent.is_mounted:
        node.is_mounted = True
        node.trigger('mount')
    else:
        @node.parent.on('mount')
        def _():
            node.parent.is_mounted = node.is_mounted = True
            node.trigger('mount')
