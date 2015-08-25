# -*- coding: utf-8 -*-

import sys
from .template import render_template
from .utils import walk

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

def parse_node(expressions, root, node):
    from .virtual_dom import is_tag_defined
    if node[0].tag == 'text':
        add_expression(expressions, node, node.html(), dict(root=root))
        return False
    else:
        for attribute, val in node[0].attrib.items():
            add_expression(expressions, node, val, dict(root=root, attr=attribute))
        return not is_tag_defined(node.attr.__riot_tag__)

def parse_expressions(expressions, root):
    walk(root.dom, lambda node: parse_node(expressions, root, node))

def update_expressions(expressions, node):
    from .tags.text import parse_markup, META as TEXT_META
    for expression in expressions:
        dom = expression['dom']
        expr = expression['expr']
        attr = expression.get('attr')
        root = expression.get('root')
        value = render_template(expr, node) or ''

        # parent = dom.parent()
        if expression.get('value') == value:
            continue

        expression['value'] = value
        if not attr:
            dom.html(value)
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
