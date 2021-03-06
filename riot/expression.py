# -*- coding: utf-8 -*-

import inspect
import json
import urwid
import sys
from copy import copy, deepcopy
from functools import wraps
from pyquery import PyQuery
from urwid.signals import disconnect_signal_by_key
from jinja2 import Environment
from .template import render_template
from .ui import IfWidget
from .ui.builtin_widgets import generate_widget
from .utils import walk, get_ui_by_path, debug

NODES = {}

def parse_markup_expression(node):
    rs = []
    for _node in PyQuery(node).contents():
        if isinstance(_node, str):
            rs.append({'expression': _node})
        elif _node.tag == 'span':
            if_ = _node.get('if')
            each_ = _node.get('each')
            class_name = _node.get('class', '')
            span_markup = parse_markup_expression(_node)
            rs.append({'expression': span_markup, 'class': class_name, 'if': if_, 'each': each_})
    return rs

def parse_document_expressions(document):
    def _is_expression(string):
        return '{' in string
    def _pop_attr(doc, attribute):
        value = doc.attr[attribute]
        doc.removeAttr(attribute)
        return value
    def _make_each_expression(doc):
        return dict(expression=_pop_attr(doc, 'each'),
                    type='each',
                    node=doc,
                    impl=doc.outer_html(),
                    impl_expressions=parse_document_expressions(doc))
    def _make_attribute_expression(doc, attr, val):
        return dict(expression=val, type='attribute', attribute=attr, node=doc)
    def _make_markup_expression(doc):
        return dict(expression=parse_markup_expression(doc), type='markup', node=doc)
    def _parse_document_expressions(doc, result, path):
        if not doc:
            return result
        if doc.attr.each:
            result.append(_make_each_expression(doc))
            return result
        for attribute, val in doc[0].attrib.items():
            _ = _is_expression(val) and result.append(
                _make_attribute_expression(doc, attribute, val))
        if doc[0].tag == 'text':
            result.append(_make_markup_expression(doc))
            return result
        elif not doc.children():
            return result
        elif doc.children():
            for index, child in enumerate(doc.children()):
                result = _parse_document_expressions(PyQuery(child), result, path + [index])
            return result
    return _parse_document_expressions(document, [], [0])

_env = Environment(variable_start_string='{', variable_end_string='}')
def evaluate_attribute_expression(expression, context):
    context = context if isinstance(context, dict) else vars(context)
    if not (expression.startswith('{') and expression.endswith('}')):
        return _env.from_string(expression).render(**context)
    return _env.compile_expression(expression[1:-1])(**context)

def evaluate_each_expression(expression, context):
    items = evaluate_attribute_expression(expression['expression'], context)
    return items

def evaluate_markup_expression(expression, context):
    def _evaluate_markup_expression(expressions, context, markups):
        if isinstance(expressions, str):
            markup = evaluate_attribute_expression(expressions, context)
            return markups + [markup]
        if isinstance(expressions, list):
            for expression in expressions:
                markups = _evaluate_markup_expression(expression, context, markups)
            return markups
        if expressions.get('if') is not None:
            condition = evaluate_attribute_expression(expressions['if'], context)
            if not condition:
                return markups
        if expressions.get('each') is not None:
            items = evaluate_attribute_expression(expressions['each'], context)
            for index, item in enumerate(items):
                loopcontext = {}
                loopcontext.update(context)
                loopcontext.update(item if isinstance(item, dict) else vars(item))
                loopcontext['loopindex'] = index
                markups = _evaluate_markup_expression(
                    expressions['expression'], loopcontext, markups)
                classname = evaluate_attribute_expression(expressions.get('class', ''), loopcontext)
                markups[-1] = (classname, markups[-1]) if classname else markups[-1]
            return markups

        markup = evaluate_markup_expression(expressions['expression'], context)
        if not markup:
            return markups
        if len(markup) == 1:
            markup = markup[0]
        classname = expressions.get('class', '')
        classname = classname and evaluate_attribute_expression(classname, context)
        markup = (classname, markup) if classname else markup
        return markups + [markup]

    markups = _evaluate_markup_expression(expression, context, [])
    if len(markups) == 1:
        return markups[0]
    if len(markups) == 0:
        return ''
    return markups

def evaluate_expression(expression, context):
    if expression['type'] == 'markup':
        return evaluate_markup_expression(expression, context)
    elif expression['type'] == 'attribute':
        return evaluate_attribute_expression(expression['expression'], context)
    elif expression['type'] == 'each':
        return evaluate_each_expression(expression, context)

def identify_document(document):
    def _make_id(path):
        return '.'.join(map(str, path))
    def _identify_document(document, path):
        if not document:
            return
        document.attr['data-riot-id'] = _make_id(path)
        if not document.children():
            return
        children_size = len(document.children())
        for index in range(children_size):
            _identify_document(document.children().eq(index), path + [index])
    _identify_document(document, [0])

def mark_dirty(node):
    if node.attr['data-riot-id'] == '0' or not node.attr['data-riot-id']:
        node.attr['data-riot-dirty'] = 'true'
        return
    node.attr['data-riot-dirty'] = 'true'
    mark_dirty(node.parent())

def render_document(vnode, expressions, context):
    for expression in expressions:
        evaluation = evaluate_expression(expression, context)
        node = expression.get('node')
        if isinstance(expression.get('value'), basestring) and expression.get('value') == evaluation:
            continue
        expression['value'] = evaluation

        if expression.get('type') == 'each':
            if expression.get('parent'):
                parent = expression.get('parent')
            else:
                parent = node.parent()
                expression['parent'] = parent
            riot_id = node.attr['data-riot-id']
            original_children = parent.children('[data-riot-id="%s"]' % riot_id)
            # 0. add placeholder
            placeholder = PyQuery('<text></text>')
            placeholder.insertBefore(original_children.eq(0))
            # 1. remove children
            original_node = original_children.clone()
            original_children.remove()
            expression['node'] = original_node
            # 2. insert children
            loopcontext = {}
            loopcontext.update(context if isinstance(context, dict) else vars(context))
            expressions_col = []
            for loop_index, item in enumerate(evaluation):
                loopcontext.update(item if isinstance(item, dict) else vars(item))
                loopcontext['loopindex'] = loop_index
                child_node = PyQuery(expression.get('impl'))
                child_node.attr['data-riot-loopindex'] = str(loop_index)
                expressions = parse_document_expressions(child_node)
                expressions_col.append((expressions, loopcontext))
                render_document(vnode, expressions, loopcontext)
                child_node.insertBefore(placeholder)
            # 3. remove placeholder
            if len(evaluation) == 0:
                placeholder.attr['data-riot-id'] = str(riot_id)
            else:
                placeholder.remove()
            mark_dirty(parent)
            generate_widget(parent)
            for expressions, loopcontext in expressions_col:
                connect_signals(vnode, expressions, loopcontext)
            continue
        if expression.get('type') == 'markup':
            node.attr['markup'] = json.dumps(evaluation)
            node.html('')
            mark_dirty(node)
            continue
        if expression.get('type') == 'attribute':
            attribute = expression.get('attribute')
            node.attr[attribute] = str(evaluation)
            mark_dirty(node)
            continue

def connect_signals(vnode, expressions, context):
    from .ui.builtin_widgets import get_widget
    for expression in expressions:
        if expression.get('type') != 'attribute' or expression.get('attribute') not in (
                'onclick', 'onchange'
        ):
            continue
        widget = get_widget(expression.get('node'))
        callback = evaluate_attribute_expression(expression['expression'], context)
        reset_event_handler(vnode, widget, expression.get('attribute')[2:], callback)

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

    if node.attr.each:
        add_expression(expressions, node, node.attr.each, dict(
            root=root, attr='each', path=path, outer_html=node.outer_html()))
        return False

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
                disconnect_signal_by_key(ui, event, ui.__dict__.pop(cache_key))
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

def update_if_expression(ui, state):
    wraps = ui
    while wraps:
        if isinstance(wraps, IfWidget):
            getattr(wraps, state and 'show' or 'hide')()
            break
        else:
            wraps = wraps.original_widget

def update_each_expression(ui, dom, items):
    debug(dom, items)

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

        if attr == 'each':
            update_each_expression(ui, dom, value)
            continue

        if attr == 'if':
            update_if_expression(ui, bool(value))

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
