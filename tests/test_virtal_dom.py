# -*- coding: utf-8 -*-

from pytest import raises
from pyquery import PyQuery
from mock import Mock
from riot import virtual_dom as vdom
from riot.observable import Observable

def test_defind_and_get_tag():
    callback = lambda *a, **kw: None
    vdom.define_tag('test', '<test></test>', callback)
    assert vdom.get_tag('test') == {
        'name': 'test',
        'html': '<test></test>',
        'fn': callback
    }

def test_pop_html():
    node = PyQuery('<test><h1></h1></test>')
    assert vdom.pop_html(node) == '<h1/>'
    assert not node.html()

def test_cache_dom():
    dom = vdom.new_dom('', '', '', '')
    dom.uuid = 'dom'
    vdom.cache_dom(dom)
    assert vdom.get_dom(dom.uuid) == dom
    dom.trigger('unmounted')
    with raises(Exception):
        assert vdom.get_dom(dom.uuid)

def test_mount_tag():
    root = PyQuery('<root></root>')
    tag = {'html': '<custom>hello world</custom>'}
    dom = vdom.mount_tag(root, tag, {})
    assert dom and dom.uuid # dom created
    assert vdom.get_dom(dom.uuid) # dom cached
    assert root.html() # mounted something

def test_mount():
    root = PyQuery('<body><div id="selector"><selected></body>')
    vdom.define_tag('test', '<test>abc</test>', lambda *a, **kw: None)
    doms = vdom.mount(root, '#selector', 'test')
    assert doms

def test_walk():
    root = PyQuery('<root><child><grandson></grandson></child></root>')
    def fn(node):
        node.addClass('walked')
        return True
    vdom.walk(root, fn)
    assert str(root) == '<root class="walked"><child class="walked"><grandson class="walked"/></child></root>'
