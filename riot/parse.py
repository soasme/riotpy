# -*- coding: utf-8 -*-

import types
import re
from pyquery import PyQuery

from .observable import Observable

def extract_logic(html):
    node = PyQuery(html)
    script = node('script').eq(0)
    script_text = script.html() or ''
    scripts = script_text.split('\n')
    scripts = [sc for sc in scripts if sc]
    if not scripts:
        return ''
    indent = 0
    for char in scripts[0]:
        if char == ' ':
            indent += 1
        else:
            break
    scripts = [sc[indent:] for sc in scripts]
    return '\n'.join(scripts)

def attach_logic_to_node(script, node, opts):
    self = node
    exec script
    fnnames = re.findall(r'^def ([a-zA-Z0-9_]+)', script, re.MULTILINE)
    localfns = locals()
    for fnname in fnnames:
        attribute = types.MethodType(localfns[fnname], node, Observable)
        setattr(node, fnname, attribute)
    if hasattr(node, 'init'):
        node.init(opts)
    return node
