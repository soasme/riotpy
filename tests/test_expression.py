# -*- coding: utf-8 -*-

from mock import ANY
from pytest import mark
from pyquery import PyQuery
from riot.expression import parse_document_expressions, evaluate_expression, parse_markup_expression

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

    ('<test><EachNode each="{ items }" /></test>', [
        {'expression': '{ items }', 'impl': '<EachNode each="{ items }"></EachNode>', 'type': 'each', 'node': ANY},
    ])
])
def test_parse_document_expressions(html, result):
    assert parse_document_expressions(PyQuery(html)) == result


@mark.parametrize('expression, context, result', [
    ('{ expr }', {'expr': 1}, 1),
    ('{ expr() }', {'expr': lambda: 1}, 1),
    ('{ expr }', {'expr': lambda: 1}, ANY), # it's a function
    ('Prefix {expr} Postfix', {'expr': 1}, 'Prefix 1 Postfix'),
    ('{ expr | lower }', {'expr': 'HELLOWORLD'}, 'helloworld'),
])
def test_evaluate_expression(expression, context, result):
    assert evaluate_expression(expression, context) == result

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
