# -*- coding: utf-8 -*-

import types
import re

from .observable import Observable

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
