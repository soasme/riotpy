# -*- coding: utf-8 -*-

from copy import deepcopy

from riot.layout import render_layout, patch_layout
from pytest import fixture

@fixture
def layout():
    return ['text', {}, 'hello world']

def test_text_tag(layout):
    el = render_layout(layout)
    assert el == [
        'text',
        {
            'markup': 'hello world',
            'align': 'left',
            'wrap': 'space',
        }
    ]

def test_text_tag_with_opts_ref(layout):
    opts = {'title': 'hello world'}
    layout[2] = '{ opts.title }'
    el = render_layout(layout, opts)
    assert el == [
        'text',
        {
            'markup': 'hello world',
            'align': 'left',
            'wrap': 'space',
        }
    ]

def test_text_tag_with_attr_ref(layout):
    layout[1]['title'] = 'hello world'
    layout[2] = '{ opts.title }'
    el = render_layout(layout)
    assert el == [
        'text',
        {
            'markup': 'hello world',
            'align': 'left',
            'wrap': 'space',
        }
    ]

def test_text_tag_with_self_ref(layout):
    layout[2] = '{ title }'
    el = render_layout(layout, {}, {'title': 'hello world'})
    assert el == [
        'text',
        {
            'markup': 'hello world',
            'align': 'left',
            'wrap': 'space',
        }
    ]

def test_update_layout(layout):
    el = [
        'text',
        {
            'markup': 'hello world',
            'wrap': 'space'
        }
    ]
    el2 = [
        'text',
        {
            'markup': 'world updated',
            'align': 'left',
            'wrap': 'any'
        }
    ]
    assert patch_layout(el, el2) == [
        # ('set_align_mode', 'left'), // ignore default
        ('set_text', 'world updated'),
        ('set_wrap_mode', 'any'),
    ]

def test_update_layout_no_change(layout):
    el = [
        'text',
        {
            'markup': 'hello world',
        }
    ]
    el2 = deepcopy(el)
    assert patch_layout(el, el2) == []
