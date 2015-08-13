# -*- coding: utf-8 -*-

from riot.layout import render_layout, patch_layout

def test_render_div():
    assert render_layout([
        'div', {}, []
    ]) == [
        'div',
        {
            'div_char': u' ',
            'top': 0,
            'bottom': 0,
        }
    ]

def test_render_div_with_div_char():
    el = render_layout([
        'div', {
            'char': u'-',
            'top': 1,
            'bottom': 1
        }, []
    ]) == [
        'div',
        {
            'div_char': u'-',
            'top': 1,
            'bottom': 1,
        }
    ]

def test_patch_div():
    # call div._invalidate()
    el1 = [
        'div',
        {
            'div_char': u' ',
            'top': 0,
            'bottom': 0,
        }
    ]
    el2 = [
        'div',
        {
            'div_char': u'-',
            'top': 1,
            'bottom': 1,
        }
    ]
    assert patch_layout(el1, el2) == [
        ('.div_char', u'-'),
        ('.top', 1),
        ('.bottom', 1),
    ]
