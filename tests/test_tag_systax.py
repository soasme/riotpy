# -*- coding: utf-8 -*-

from pytest import raises
from mock import ANY


def test_html_is_defined_first():
    assert compile_tag('<tag><text></text></tag>') == {
        'name': 'tag',
        'layout': [
            ['text', {}, []], # tag-name, attributes, children
        ], # layout is a list of tags
        'logic': '',
    }

def test_logic_is_enclosed_inside_an_optional_script_tag():
    assert compile_tag('<tag><script>self.text = "text"</script></tag>') == {
        'name': 'tag',
        'layout': [],
        'logic': 'self.text = "text"'
    }

def test_without_the_script_tag_the_python_starts_where_the_last_html_tag_ends():
    assert compile_tag('<tag><text>{ text }</text>self.text = "text";</tag>') == {
        'name': 'tag',
        'layout': [
            ['text', {}, '{ text }'],
        ],
        'logic': 'self.text = "text";',
    }

def test_custom_tag_can_be_empty():
    assert compile_tag('<tag></tag>') == {
        'name': 'tag',
        'layout': [],
        'logic': '',
    }

def test_quota_attributes():
    assert compile_tag('<tag><text bar="{ baz }"></text></tag>') == {
        'name': 'tag',
        'logic': '',
        'layout': [
            ['text', {"bar": "{ baz }"}, []],
        ],
    }

def test_shorthand_syntax_for_class_name():
    assert compile_tag('<tag><text class="{ complete: False }"></text></tag>') == {
        'name': 'tag',
        'logic': '',
        'layout': [
            ['text', {"class": "{ complete: False }"}, []],
        ],
    }

def test_self_closing_tags_are_supported():
    assert compile_tag('<tag><text /></tag>') == {
        'name': 'tag',
        'layout': [
            ['text', {}, []],
        ],
        'logic': '',
    }

def test_tag_definition_in_tag_files_always_starts_on_the_beginning():
    assert compile_tag('''<tag>
</tag>''')
    assert compile_tag('''<tag></tag>''')
    with raises(Exception):
        assert compile_tag('''
    <tag>
    </tag>''')

def test_tag_styling():
    assert compile_tag('''
<tag>
    <text>{ text }</text>
    <style>
        tag { mono: default; }
        tag text { background-color: white; }
    </style>
</tag>''') == {
        'name': 'tag',
        'layout': [
            ['text', {}, '{ text }'],
        ],
        'logic': '',
        'style': [
            ('tag', {
                'mono': 'default',
            }),
            ('tag text', {
                'background-color': 'white',
            }),
        ]
    }

def test_scoped_styling():
    assert compile_tag('''
<tag>
    <text>{ text }</text>
    <style>
        :scope { mono: default; }
        text { background-color: white; }
    </style>
</tag>''') == {
        'name': 'tag',
        'layout': [
            ['text', {}, '{ text }'],
        ],
        'logic': '',
        'style': [
            ('tag', {
                'mono': 'default',
            }),
            ('tag text', {
                'background-color': 'white',
            }),
        ]
    }

