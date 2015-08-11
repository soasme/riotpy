# -*- coding: utf-8 -*-

from riot.layout import render_layout

def test_render_div():
    el = render_layout([
        'div', {}, []
    ])
    assert el
    assert el.uuid
    assert el.rows((10, )) == 1
    assert el.render((10, )).text == [
        u'          ',
    ]

def test_render_div_with_div_char():
    el = render_layout([
        'div', {
            'char': u'-',
            'top': 1,
            'bottom': 1
        }, []
    ])
    assert el
    assert el.rows((10, )) == 3 # top line + --------- + bottom line
    assert el.render((10, )).text == [
        '          ',
        '----------',
        '          ',
    ]
