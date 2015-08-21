# -*- coding: utf-8 -*-

from pytest import raises
from pyquery import PyQuery
from mock import Mock
from riot import virtual_dom as vdom
from riot.observable import Observable

def test_defind_and_get_tag():
    vdom.define_tag('test', '<test></test>')
    assert vdom.get_tag('test') == {
        'name': 'test',
        'html': '<test></test>',
    }

def test_pop_html():
    node = PyQuery('<test><h1></h1></test>')
    assert vdom.pop_html(node) == '<h1/>'
    assert not node.html()

def test_cache_dom():
    dom = Observable()
    dom.uuid = 'dom'
    vdom.cache_dom(dom)
    assert vdom.get_dom(dom.uuid) == dom
    dom.trigger('unmounted')
    with raises(Exception):
        assert vdom.get_dom(dom.uuid)

def test_mount_tag():
    root = PyQuery('<root></root>')
    tag = {'name': 'custom', 'html': '<custom><text>{opts.txt}</text></custom>'}
    dom = vdom.mount_tag(root, tag, {'txt': 'hello world'})
    assert dom and dom.uuid # dom created
    assert vdom.get_dom(dom.uuid) # dom cached
    assert root.html() # mounted something

def test_mount():
    root = PyQuery('<body><div id="selector"></div></body>')
    vdom.define_tag('test', '<test><text>_</text></test>')
    doms = vdom.mount(root, '#selector', 'test')
    assert doms
    assert root('#selector').attr.__riot_tag__ == 'test'
