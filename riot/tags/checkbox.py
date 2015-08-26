# -*- coding: utf-8 -*-

from urwid import CheckBox

def parse_tag_from_node(node):
    label = node.attr.label or ''
    state = bool(node.attr.state or '')
    return CheckBox(label=label, state=state)
META = {
    'attribute_methods': {
        'state': ('set_state', bool),
    }
}
