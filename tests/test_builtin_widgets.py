# -*- coding: utf-8 -*-

import urwid
import json
from pyquery import PyQuery
import riot.ui.builtin_widgets as builtin

def test_cache_widget():
    text = PyQuery('<text/>')
    text_w1 = builtin.generate_widget(text)
    text_w2 = builtin.generate_widget(text)
    assert text_w1 == text_w2

def test_generate_text_widget():
    text = PyQuery('<text/>')
    text.attr.markup = json.dumps('hello world')
    text = builtin.generate_widget(text)
    assert text.__class__ == urwid.Text
    assert text.text == 'hello world'

def test_generate_edit_widget():
    edit = PyQuery('<edit caption="Y/n?" edit_text="yes" edit_pos="3"/>')
    edit = builtin.generate_widget(edit)
    assert edit.__class__ == urwid.Edit
    assert edit.caption == 'Y/n?'
    assert edit.edit_text == 'yes'
    assert edit.edit_pos == 3

def test_generate_checkbox_widget():
    checkbox = PyQuery('<check-box label="label" state="on" />')
    checkbox = builtin.generate_widget(checkbox)
    assert checkbox.__class__ == urwid.CheckBox
    assert checkbox.label == 'label'
    assert checkbox.state

def test_generate_attrmap_widget():
    attrmap = PyQuery('<attr-map attr_map="bright"><text></text></attr-map>')
    attrmap = builtin.generate_widget(attrmap)
    assert attrmap.__class__ == urwid.AttrMap
    assert attrmap.attr_map == {None: 'bright'}
    assert attrmap.original_widget.__class__ == urwid.Text
