# -*- coding: utf-8 -*-

from riot.layout import render_layout

def test_render_div():
    el = render_layout([
        ['div', {}, []],
    ])
    assert el
    assert el.uuid
    assert 'Divider' in str(el)
