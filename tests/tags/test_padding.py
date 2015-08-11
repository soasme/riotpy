# -*- coding: utf-8 -*-

from riot.layout import render_layout

def test_padding_left():
    el = render_layout([
        'text', {
            'style': 'padding-left: 2',
        },
        u'text',
    ])
    assert el
    assert el.render((6, )).text == [
        '  text'
    ]

def test_padding_right():
    el = render_layout([
        'text', {
            'style': 'padding-right: 2',
        },
        u'text',
    ])
    assert el
    assert el.render((6, )).text == [
        'text  '
    ]

def test_padding_align_left():
    el = render_layout([
        'text', {
            'style': 'padding-align: left',
        },
        u'text',
    ])
    assert el
    assert el.render((10, )).text == [
        'text      '
    ]

def test_padding_align_right():
    el = render_layout([
        'text', {
            'style': 'padding-align: left',
        },
        u'text',
    ])
    assert el
    assert el.render((10, )).text == [
        '      text'
    ]

def test_padding_align_center():
    el = render_layout([
        'text', {
            'style': 'padding-align: center',
        },
        u'text',
    ])
    assert el
    assert el.render((10, )).text == [
        '   text   '
    ]

def test_padding_align_zero_percentage():
    el = render_layout([
        'text', {
            'style': 'padding-align: 0%',
        },
        u'text',
    ])
    assert el
    assert el.render((10, )).text == [
        'text      '
    ]

def test_padding_align_hundred_percentage():
    el = render_layout([
        'text', {
            'style': 'padding-align: 100%',
        },
        u'text',
    ])
    assert el
    assert el.render((10, )).text == [
        '      text'
    ]

def test_padding_align_twenty_percentage():
    el = render_layout([
        'text', {
            'style': 'padding-align: 20%',
        },
        u'text',
    ])
    assert el
    assert el.render((10, )).text == [
        '  text    '
    ]

def test_padding_width():
    el = render_layout([
        'text', {
            'style': 'padding-width: 2',
        },
        u'text',
    ])
    assert el
    assert el.render((3, )).text == [
        'te ',
        'xt ',
    ]

def test_padding_width_pack():
    el = render_layout([
        'text', {
            'style': 'padding-width: pack',
        },
        u'text\nlatex',
    ])
    assert el
    assert el.render((6, )).text == [
        ' text',
        'latex',
    ]

def test_padding_width_relative():
    el = render_layout([
        'text', {
            'style': 'padding-width: 20%',
        },
        u'abc',
    ])
    assert el
    assert el.render((10, )).text == [
        'ab        ',
        'c         ',
    ]
