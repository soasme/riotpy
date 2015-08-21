# -*- coding: utf-8 -*-

from pyquery import PyQuery
import riot.virtual_dom as vdom
from riot.utils import walk

def test_walk():
    root = PyQuery('<root><child><grandson></grandson></child></root>')
    def fn(node):
        node.addClass('walked')
        return True
    walk(root, fn)
    assert str(root) == '<root class="walked"><child class="walked"><grandson class="walked"/></child></root>'
