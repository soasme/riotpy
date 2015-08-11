# -*- coding: utf-8 -*-

import re
from uuid import uuid4
from urwid import (
    Text, Divider
)

def get_attribute(render_data, variable):
    levels = variable.split('.')
    r = render_data
    for level in levels:
        r = r[level]
    return r

variable_re = re.compile(r'({\s*.*\s*})')
def render_template(text, render_data):
    variables = variable_re.findall(text)
    variables = {var[1:-1].strip(): var for var in variables}
    for variable in variables:
        text = text.replace(variables[variable], get_attribute(render_data, variable))
    return text

def render_text_layout(attributes, text, opts, ref):
    class_ = attributes.get('class', '')
    classes = [] if not class_ else [class_]
    align = attributes.get('align', 'left')
    wrap = attributes.get('wrap', 'any')
    render_data = dict(ref)
    render_data['opts'] = opts
    if isinstance(text, str):
        markup = render_template(text, render_data)
    elif isinstance(text, list):
        markup = [render_template(tpl, render_data) for tpl in text if tpl]
    elif isinstance(text, tuple):
        markup = render_template(text[1], render_data)
    return Text(markup, align=align, wrap=wrap)

def render_div_layout(attributes, text, opts, ref):
    div_char = attributes.get('char', u' ')
    top = int(attributes.get('top', 0))
    bottom = int(attributes.get('bottom', 0))
    return Divider(div_char, top, bottom)

RENDERERS = {
    'text': render_text_layout,
    'div': render_div_layout,
}

def render_layout(layout, opts={}, ref={}):
    tag_name, attributes, children = layout
    el = RENDERERS[tag_name](attributes, children, opts, ref)
    el.uuid = uuid4()
    return el

