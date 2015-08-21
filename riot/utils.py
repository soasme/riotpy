# -*- coding: utf-8 -*-

def walk(root, function):
    if not root:
        return
    if not function(root):
        return
    for child in root.children().items():
        walk(child, function)
