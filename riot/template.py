# -*- coding: utf-8 -*-

import re

def get_attribute(render_data, variable):
    levels = variable.split('.')
    r = render_data
    for level in levels:
        r = r.get(level) or {}
    if not r:
        return ''
    return r

variable_re = re.compile(r'({\s*.*\s*})')

def is_function(text, node):
    fnname = render_template(text, node)
    return hasattr(fnname, node)

def render_template(text, render_data):
    variables = variable_re.findall(text)
    variables = {var[1:-1].strip(): var for var in variables}
    for variable in variables:
        text = text.replace(variables[variable], get_attribute(render_data, variable))
    return text
