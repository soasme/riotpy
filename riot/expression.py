# -*- coding: utf-8 -*-

import urwid
import sys
from .template import render_template
from .utils import walk, get_ui_by_path

NODES = {}

def parse_children(children, root, vnode):
    # walk(root, lambda node: parse_node_children(children, node, vnode))
    pass

def add_expression(expressions, dom, val, extra={}):
    if '{' in val:
        expression = dict(
            dom=dom,
            expr=val
        )
        expression.update(extra or {})
        expressions.append(expression)

def parse_node(expressions, root, node, path):
    from .virtual_dom import is_tag_defined
    if node[0].tag == 'text':
        add_expression(expressions, node, node.html(), dict(root=root, attr='inner_html', path=path))
        return False
    else:
        for attribute, val in node[0].attrib.items():
            add_expression(expressions, node, val, dict(root=root, attr=attribute, path=path))
        return not is_tag_defined(node.attr.__riot_tag__)

def parse_expressions(expressions, root):
    walk(root.dom, lambda node, path: parse_node(expressions, root, node, path))

def update_expressions(expressions, node):
    from .tags.text import parse_markup, META as TEXT_META
    for expression in expressions:
        dom = expression['dom']
        path = expression.get('path')
        ui = path and get_ui_by_path(node.ui, path)
        expr = expression['expr']
        attr = expression.get('attr')
        root = expression.get('root')
        value = render_template(expr, node) or ''

        # parent = dom.parent()
        if expression.get('value') == value:
            continue

        # text
        expression['value'] = value
        if attr == 'inner_html':
            dom.html(value)
            markup = parse_markup(value) or ''
            getattr(ui, TEXT_META['attribute_methods']['inner_html'])(markup)
            continue

        if attr == 'onclick' and callable(value):
            if '_sig_on_click' in ui.__dict__:
                key = ui.__dict__.pop('_sig_on_click')
                urwid.disconnect_by_key(ui, 'click', key)
            ui.__dict__['_sig_on_click'] = urwid.connect_signal(ui, 'click', value)
            continue

        if attr == 'onchange' and callable(value):
            if '_sig_on_change' in ui.__dict__:
                key = ui.__dict__.pop('_sig_on_change')
                urwid.disconnect_by_key(ui, 'change', key)
            ui.__dict__['_sig_on_change'] = urwid.connect_signal(ui, 'change', value)
            continue

        dom.attr[attr] = ''
        if callable(value):
            origin_callback = getattr(node.ui, attr)
            def new_callback(*args, **kwargs):
                ret = value(*args, **kwargs)
                if not ret:
                    return origin_callback(*args, **kwargs)
                return ret
            setattr(node.ui, attr, new_callback)
            continue
        getattr(node.ui, 'set_%s' % attr)(value)
