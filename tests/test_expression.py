# -*- coding: utf-8 -*-

from mock import ANY
from pytest import mark
from pyquery import PyQuery
from riot.expression import parse_document_expressions, evaluate_attribute_expression, parse_markup_expression, identify_document, evaluate_markup_expression, evaluate_each_expression, mark_dirty, render_document

@mark.parametrize('html, result', [
    ('<test></test>', []),

    ('<test attr1="{ value1 }" attr2="{ value2 }" attr3="value3"></test>', [
        {'expression': '{ value1 }', 'attribute': 'attr1', 'type': 'attribute', 'node': ANY},
        {'expression': '{ value2 }', 'attribute': 'attr2', 'type': 'attribute', 'node': ANY},
    ]),

    ('<test><child attr="{ value }"></child></test>', [
        {'expression': '{ value }', 'attribute': 'attr', 'type': 'attribute', 'node': ANY},
    ]),

    ('<text>{ markup }</text>', [
        {'expression': [{'expression': '{ markup }'}], 'type': 'markup', 'node': ANY},
    ]),

    ('<test><each-node each="{ items }" title="{ title }"></test>', [
        {
            'expression': '{ items }',
            'impl': '<each-node title="{ title }"></each-node>',
            'type': 'each',
            'node': ANY,
            'impl_expressions': [
                {'expression': '{ title }', 'type': 'attribute', 'attribute': 'title', 'node': ANY}
            ]
        },
    ])
])
def test_parse_document_expressions(html, result):
    assert parse_document_expressions(PyQuery(html)) == result


@mark.parametrize('text, result', [
    ('<text/>', []),
    ('<text>hello</text>', [{'expression': 'hello'}]),
    ('<text>{ hello }</text>', [{'expression': '{ hello }'}]),
    ('<text>{ prefix }<span class="test" if="{ mid }">{ mid }</span>{ postfix }</text>', [
        {'expression': '{ prefix }'},
        {'expression': [{'expression': '{ mid }'}], 'class': 'test', 'if': '{ mid }', 'each': None},
        {'expression': '{ postfix }'},
    ]),
    ('<text><span each="{ items }">{ title }</span></text>', [
        {'expression': [
            {'expression': '{ title }'}
        ], 'class': '', 'if': None, 'each': '{ items }'}
    ]),
])
def test_parse_markup_expression(text, result):
    assert parse_markup_expression(PyQuery(text)) == result

@mark.parametrize('expression, context, result', [
    ('{ expr }', {'expr': 1}, 1),
    ('{ expr() }', {'expr': lambda: 1}, 1),
    ('{ expr }', {'expr': lambda: 1}, ANY), # it's a function
    ('Prefix {expr} Postfix', {'expr': 1}, 'Prefix 1 Postfix'),
    ('{ expr | lower }', {'expr': 'HELLOWORLD'}, 'helloworld'),
])
def test_evaluate_expression(expression, context, result):
    assert evaluate_attribute_expression(expression, context) == result


@mark.parametrize('document, result', [
    ('<a></a>', '<a data-riot-id="0"></a>'),
    ('<a><b/></a>', '<a data-riot-id="0"><b data-riot-id="0.0"></b></a>')
])
def test_identify_document(document, result):
    root = PyQuery(document)
    identify_document(root)
    assert root.outer_html() == result

@mark.parametrize('expr, context, markups', [
    ([{'expression': 'hello world'}], {}, 'hello world'),
    ([{'expression': '{ title }'}], {'title': 'hello world'}, 'hello world'),
    ([{'expression': '{ title }', 'if': '{ false }'}], {'title': 'hello world', 'false': False}, ''),
    ([{'expression': '{ title }', 'if': '{ true }'}], {'title': 'hello world', 'true': True}, 'hello world'),
    ([{'expression': '{ title }', 'each': '{ items }'}], {'items': [{'title': 'hello'}, {'title': 'world'}]}, ['hello', 'world']),
    ([{'expression': '{ title }', 'class': 'class'}], {'title': 'hello world'}, ('class', 'hello world')),
    ([{'expression': [{'expression': '{ title }', 'class': '{ inner }'}], 'class': '{ outer }'}], {'title': 'hello world', 'inner': 'inner', 'outer': 'outer'}, ('outer', ('inner', 'hello world')))
])
def test_evaluate_markup_expression(expr, context, markups):
    assert evaluate_markup_expression(expr, context) == markups

@mark.parametrize('expr, context, result', [
    ({'expression': '{ items }', 'type': 'each', 'impl_expressions': [
        {'expression': [{'expression': '{ title }'}], 'type': 'markup'}
    ]},
     {'items': [{'title': 'hello'}, {'title': 'world'}]},
     [{'title': 'hello'}, {'title': 'world'}]),
])
def test_evaluate_each_expression(expr, context, result):
    assert evaluate_each_expression(expr, context) == result


def test_mark_dirty():
    node = PyQuery('<a data-riot-id="0"><b data-riot-id="0.0"><c data-riot-id="0.0.0"></c></b></a>')
    mark_dirty(node.children('b'))
    assert node.attr['data-riot-dirty'] == 'true'
    assert node.children('b').attr['data-riot-dirty'] == 'true'
    assert not node.children('c').attr['data-riot-dirty']

def test_render_attribute_to_document():
    document = PyQuery('<a attribute="{ value }" data-riot-id="0"></a>')
    expression =  {'expression': '{ value }', 'attribute': 'attribute', 'type': 'attribute', 'node': document}
    render_document([expression], {'value': 'value'})
    assert document.outer_html() == '<a attribute="value" data-riot-id="0" data-riot-dirty="true"></a>'
    render_document([expression], {'value': 1})
    assert document.outer_html() == '<a attribute="1" data-riot-id="0" data-riot-dirty="true"></a>'

def test_render_markup_to_document():
    document = PyQuery('<custom data-riot-id="0"><text data-riot-id="0.0"><span class="name">{ name}</span><span class="greet">{ greet }</span></text></custom>')
    expressions = parse_document_expressions(document)
    render_document(expressions, {'name': '@ainesmile', 'greet': 'I love you.'})
    assert document.outer_html() == '<custom data-riot-id="0" data-riot-dirty="true"><text data-riot-id="0.0" data-riot-dirty="true"></text></custom>'
    assert expressions[0]['value'] == [(u'name', '@ainesmile'), (u'greet', 'I love you.')]
    render_document(expressions, {'name': '@soasme', 'greet': 'I love you, too.'})
    assert expressions[0]['value'] == [(u'name', '@soasme'), (u'greet', 'I love you, too.')]

def test_render_each_to_document():
    document = PyQuery('<custom data-riot-id="0"><button label="{ label }" each="{ items }" data-riot-id="0.0"></button></custom>')
    expressions = parse_document_expressions(document)
    render_document(expressions, {'items': [{'label': 'first'}, {'label': 'second'}]})
    assert document.attr['data-riot-dirty'] == 'true'
    assert len(document.children()) == 2
    assert document('button').eq(0).attr.label == 'first'
    assert document('button').eq(1).attr.label == 'second'
