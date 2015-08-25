# -*- coding: utf-8 -*-

from uuid import uuid4
from urwid import WidgetDecoration, SolidFill, Filler, Text, ExitMainLoop
from pyquery import PyQuery
from .observable import Observable
from .expression import update_expressions, parse_expressions
from .template import render_template
from .parse import extract_logic, attach_logic_to_node

def new_node(impl, inner, **kwargs):
    node = Observable()
    node.uuid = uuid4()
    node.impl = impl
    node.inner = inner
    node.children = []
    node.expressions = []
    node.opts = dict(kwargs.get('opts') or {})
    node.root = kwargs.get('root')
    node.parent = kwargs.get('parent')
    node.dom = make_dom(node)
    node.exit = quit
    node.update = lambda data: update_node(node, data)
    node.mount = lambda: mount_node(node)
    node.unmount = lambda: unmount_node(node)
    return node

def new_child_node(impl, dom, root):
    node = new_node(impl, dom.html(), )
    return node

def quit(*args, **kwargs):
    raise ExitMainLoop()

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
    return node.opts

def extend_node(node, data):
    node.opts = render_opts(node)
    for key, value in data.items():
        setattr(node, key, value)

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
    from .tags.tags import parse_tag_from_node
    node.opts = render_opts(node)
    node.ui = parse_tag_from_node(node.dom.children().eq(0))
    logic = extract_logic(node.impl.get('html'))
    attach_logic_to_node(logic, node, node.opts)
    _ = node.root and parse_expressions(node.expressions, node)
    mount_children_nodes(node)
    node.trigger('premount')
    node.update(node.opts)
    node.root.html(node.dom.html())

    if not node.parent or node.parent.is_mounted:
        node.is_mounted = True
        node.trigger('mount')
    else:
        def on_parent_mounted():
            node.parent.is_mounted = node.is_mounted = True
            node.trigger('mount')
        node.parent.on('mount', on_parent_mounted)
