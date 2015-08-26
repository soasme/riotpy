# -*- coding: utf-8 -*-

import urwid
import sys
from functools import wraps
from .template import render_template
from .ui import IfWidget
from .utils import walk, get_ui_by_path, debug

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

    for attribute, val in node[0].attrib.items():
        add_expression(expressions, node, val, dict(root=root, attr=attribute, path=path))

    if node[0].tag == 'text':
        add_expression(expressions, node, node.html(), dict(root=root, attr='inner_html', path=path))
        return False

    return not is_tag_defined(node.attr.__riot_tag__)

def parse_expressions(expressions, root):
    walk(root.dom, lambda node, path: parse_node(expressions, root, node, path))

def cache_event_handler(cache_pattern):
    def deco(f):
        @wraps(f)
        def _deco(node, ui, event, handler):
            cache_key = cache_pattern.format(event=event)
            _ = cache_key in ui.__dict__ and \
                    urwid.disconnect_by_key(ui, event, ui.__dict__.pop(cache_key))
            handler_key = f(node, ui, event, handler)
            ui.__dict__[cache_key] = handler_key
            return handler_key
        return _deco
    return deco

@cache_event_handler('_sig_on_{event}')
def reset_event_handler(node, ui, event, handler):
    def _handler(*args, **kwargs):
        r = handler(*args, **kwargs)
        node.update({})
        return r
    return urwid.connect_signal(ui, event, _handler)

def update_expressions(expressions, node):
    from .tags.text import parse_markup, META as TEXT_META
    from .tags.checkbox import META as CHECKBOX_META
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

        if attr == 'if':
            value = bool(value)
            wraps = ui
            while wraps:
                if isinstance(wraps, IfWidget):
                    getattr(wraps, value and 'show' or 'hide')()
                    break
                else:
                    wraps = wraps.original_widget
            continue

        # text
        expression['value'] = value
        if attr == 'inner_html':
            dom.html(value)
            markup = parse_markup(value) or ''
            getattr(ui, TEXT_META['attribute_methods']['inner_html'])(markup)
            continue


        if callable(value):
            if attr in ('onclick', 'onchange'):
                reset_event_handler(node, ui, attr[2:], value)
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
        if isinstance(ui, urwid.CheckBox) and attr in CHECKBOX_META['attribute_methods']:
            method, filter = CHECKBOX_META['attribute_methods'][attr]
            getattr(ui, method)(filter(value))
        else:
            getattr(ui, 'set_%s' % attr)(value)
