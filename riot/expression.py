# -*- coding: utf-8 -*-

from .virtual_dom import is_tag_defined
from .template import render_template
from .utils import walk

def add_expression(expressions, dom, val, extra={}):
    if '{' in val:
        expression = dict(
            dom=dom,
            expr=val
        )
        expression.update(extra or {})
        expressions.append(expression)

def parse_node(expressions, node):
    if node[0].tag == 'text':
        add_expression(expressions, node, node.html())
        return False
    else:
        for attribute, val in node[0].attrib.items():
            add_expression(expressions, node, val, dict(attr=attribute))
        return not is_tag_defined(node.attr.__riot_tag__)

def parse_expressions(expressions, root):
    walk(root, lambda node: parse_node(expressions, node))

def update_expressions(expressions, node):
    for expression in expressions:
        # dom = expression['dom']
        expr = expression['expr']
        attr = expression.get('attr')
        value = render_template(expr, node) or ''
        # parent = dom.parent()
        if expression.get('value') == value:
            continue
        expression['value'] = value
        if not attr:
            node.html(value)
            continue
        node.attr[attr] = ''
        if callable(getattr(node, value)):
            raise NotImplementedError
        setattr(node.ui, attr, value)
