# -*- coding: utf-8 -*-

from functools import wraps
from urwid import AttrMap
from pyquery import PyQuery

from ..ui import IfWidget

def convert_string_to_node(string):
    return PyQuery(string)

def detect_class(f):
    @wraps(f)
    def _detect_class(*args, **kwargs):
        pq = kwargs.get('node', args[0])
        class_name = pq.attr['class'] or ''
        class_names = class_name.split(' ')
        node = f(*args, **kwargs)
        for class_name in class_names:
            if class_name:
                node = AttrMap(node, class_name)
        return node
    return _detect_class

def detect_if(f):
    @wraps(f)
    def _detect_class(*args, **kwargs):
        pq = kwargs.get('node', args[0])
        if_ = pq.attr['if'] or ''
        state = if_ == 'True'
        node = f(*args, **kwargs)
        if if_:
            node = IfWidget(node, state=state)
        return node
    return _detect_class
