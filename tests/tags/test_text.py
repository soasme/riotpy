# -*- coding: utf-8 -*-

from riot.layout import render_layout
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
        }
    ]

def test_text_tag_with_opts_ref(layout):
    opts = {'title': 'Hello World'}
    layout[2] = '{ opts.title }'
    el = render_layout(layout, opts)
    assert el == [
        'text',
        {
            'markup': 'hello world',
        }
    ]

def test_text_tag_with_self_ref():
    layout[2] = '{ title }'
    el = render_layout(layout, {}, {'title': 'hello world'})
    assert el == [
        'text',
        {
            'markup': 'hello world',
        }
    ]

def test_text_tag_with_attr(layout):
    layout[1]['title'] = 'hello world'
    layout[2] = '{ opts.title }'
    assert el == [
        'text',
        {
            'markup': 'hello world',
        }
    ]

def test_update_layout(layout):
    modified = deepcopy(layout)
    modified[1]['align'] = 'left'
    modified[1]['wrap'] = 'space'
    modified[2] = 'world updated'
    el = [
        'text',
        {
            'markup': 'hello world',
        }
    ]
    el, patch = update_layout(el, layout)
    assert el == [
        'text',
        {
            'markup': 'world updated',
        }
    ]
    assert patch == [
        ('set_align_mode', 'left'),
        ('set_wrap_mode', 'space'),
        ('set_text', 'world updated'),
    ]

def test_update_layout_no_change(layout):
    el = [
        'text',
        {
            'markup': 'hello world',
        }
    ]
    el_, patch = update_layout(el, layout)
    assert el == el_
    assert patch == []

def test_update_layout_by_opts(layout):
    modified = deepcopy(layout)
    modified[2] = '{ opts.title }'
    el = [
        'text',
        {
            'markup': 'hello world',
        }
    ]
    el, patch = update_layout(el, layout, {'title': 'world updated'})
    assert el == [
        'text',
        {
            'markup': 'world updated',
        }
    ]
    assert patch == [
        ('set_text', 'world updated'),
    ]

def test_update_layout_by_self(layout):
    modified = deepcopy(layout)
    modified[2] = '{ title }'
    el = [
        'text',
        {
            'markup': 'hello world',
        }
    ]
    el, patch = update_layout(el, layout, {}, {'title': 'world updated'})
    assert el == [
        'text',
        {
            'markup': 'world updated',
        }
    ]
    assert patch == [
        ('set_text', 'world updated'),
    ]
