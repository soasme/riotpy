# -*- coding: utf-8 -*-

import re
from jinja2 import Environment
from .observable import Observable

def get_attribute(render_data, variable):
    levels = variable.split('.')
    r = render_data
    for level in levels:
        if hasattr(r, level):
            r = getattr(r, level)
        else:
            r = r.get(level) or {}
    if not r:
        return ''
    return r

variable_re = re.compile(r'({\s*.*\s*})')

def is_function(text, node):
    fnname = render_template(text, node)
    return hasattr(fnname, node)

env = Environment(variable_start_string='{', variable_end_string='}')

def render_template(text, render_data):
    if not (text.startswith('{') and text.endswith('}')):
        return env.from_string(text).render(**vars(render_data))

    expr = text[1:-1]
    return env.compile_expression(expr)(**vars(render_data))

    variables = variable_re.findall(text)
    variables = {var[1:-1].strip(): var for var in variables}
    for variable in variables:
        rendered = get_attribute(render_data, variable)
        if callable(rendered):
            return rendered
        text = text.replace(variables[variable], rendered)
    return text
