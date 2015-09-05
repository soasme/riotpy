# -*- coding: utf-8 -*-

import riot.virtual_node as vnode
from riot.observable import Observable

def test_new_node():
    impl = {'html': '<custom><text>_</text></custom>', 'name': 'custom', 'fn': lambda *a, **kw: None}
    node = vnode.new_node(impl, '')
    assert node
    assert node.uuid
    for life_cycle_function in ('update', 'mount', 'unmount'):
        assert getattr(node, life_cycle_function)
