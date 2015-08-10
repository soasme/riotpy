# -*- coding: utf-8 -*-

import urwid

def test_text_tag():
    el = render_layout(['text', {
        'align': 'left',
        'wrap': 'space',
    }, 'Hello World'])
    assert el
    assert el.uuid
    assert str(el) == "<Text flow widget 'Hello World' align='right' wrap='any'>"
    assert el.text == 'Hello World'

def test_text_tag_with_opts_ref():
    opts = {'title': 'Hello World'}
    el = render_layout(['text', {
        'align': 'left',
        'wrap': 'space',
    }, '{ opts.title }'], opts)
    assert el.text == 'Hello World'
    assert el.uuid

def test_text_tag_with_self_ref():
    el = render_layout(['text', {
        'align': 'left',
        'wrap': 'space',
    }, '{ title }'], {}, {'title': 'Hello World'})
    assert el.text == 'Hello World'
    assert el.uuid
