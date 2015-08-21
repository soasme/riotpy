# -*- coding: utf-8 -*-


from .template import render_template
from .utils import walk

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

def parse_node(expressions, node):
    from .virtual_dom import is_tag_defined
    if node[0].tag == 'text':
        add_expression(expressions, node, node.html())
        return False
    else:
        for attribute, val in node[0].attrib.items():
            add_expression(expressions, node, val, dict(attr=attribute))
        return not is_tag_defined(node.attr.__riot_tag__)

def parse_expressions(expressions, root):
    walk(root.dom, lambda node: parse_node(expressions, node))

def update_expressions(expressions, node):
    for expression in expressions:
        dom = expression['dom']
        expr = expression['expr']
        attr = expression.get('attr')
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
        getattr(node.ui.original_widget, 'set_%s' % attr)(value)
