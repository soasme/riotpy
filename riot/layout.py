# -*- coding: utf-8 -*-

import re
from copy import deepcopy
from uuid import uuid4
from urwid import (
    Text, Divider
)

def get_attribute(render_data, variable):
    levels = variable.split('.')
    r = render_data
    for level in levels:
        r = r.get(level) or {}
    if not r:
        return ''
    return r

variable_re = re.compile(r'({\s*.*\s*})')
def render_template(text, render_data):
    variables = variable_re.findall(text)
    variables = {var[1:-1].strip(): var for var in variables}
    for variable in variables:
        text = text.replace(variables[variable], get_attribute(render_data, variable))
    return text

def render_text_layout(attributes, text, opts, ref):
    align = attributes.pop('align', 'left')
    wrap = attributes.pop('wrap', 'space')
    render_data = dict(ref)
    render_data['opts'] = deepcopy(opts)
    render_data['opts'].update(attributes)
    if isinstance(text, str):
        markup = render_template(text, render_data)
    elif isinstance(text, list):
        markup = [render_template(tpl, render_data) for tpl in text if tpl]
    elif isinstance(text, tuple):
        markup = render_template(text[1], render_data)
    return [
        'text',
        {
            'markup': markup,
            'align': align,
            'wrap': wrap,
        }
    ]

def patch_text_layout(el1, el2):
    if el1[1].get('markup', '') != el2[1].get('markup', ''):
        yield ('set_text', el2[1]['markup'])
    if el1[1].get('align', 'left') != el2[1].get('align', 'left'):
        yield ('set_align_mode', el2[1].get('align', 'left'))
    if el1[1].get('wrap', 'space') != el2[1].get('wrap', 'space'):
        yield ('set_wrap_mode', el2[1].get('wrap', 'space'))

def render_div_layout(attributes, text, opts, ref):
    div_char = attributes.get('char', u' ')
    top = attributes.get('top', 0)
    bottom = attributes.get('bottom', 0)
    return [
        'div',
        {
            'div_char': div_char,
            'top': top,
            'bottom': bottom,
        }
    ]
    return Divider(div_char, top, bottom)

def patch_div_layout(el1, el2):
    if el1[1].get('div_char', u' ') != el2[1].get('div_char', u' '):
        yield ('.div_char', el2[1].get('div_char', u' '))
    if el1[1].get('top', 0) != el2[1].get('top', 0):
        yield ('.top', el2[1].get('top', 0))
    if el1[1].get('bottom', 0) != el2[1].get('bottom', 0):
        yield ('.bottom', el2[1].get('bottom', 0))

RENDERERS = {
    'text': render_text_layout,
    'div': render_div_layout,
}

PATCHERS = {
    'text': patch_text_layout,
    'div': patch_div_layout,
}

def render_layout(layout, opts={}, ref={}):
    tag_name, attributes, children = layout
    return RENDERERS[tag_name](attributes, children, opts, ref)

def patch_layout(el1, el2):
    assert(el1[0] == el2[0])
    return [_ for _ in PATCHERS[el2[0]](el1, el2)]
