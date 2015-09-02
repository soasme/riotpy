# -*- coding: utf-8 -*-

from mock import ANY
from pytest import mark
from pyquery import PyQuery
from riot.expression import parse_document_expressions, evaluate_expression

@mark.parametrize('html, result', [
    ('<test></test>', []),

    ('<test attr1="{ value1 }" attr2="{ value2 }" attr3="value3"></test>', [
        {'expression': '{ value1 }', 'attribute': 'attr1', 'type': 'attribute', 'node': ANY},
        {'expression': '{ value2 }', 'attribute': 'attr2', 'type': 'attribute', 'node': ANY},
    ]),

    ('<test><child attr="{ value }"></child></test>', [
        {'expression': '{ value }', 'attribute': 'attr', 'type': 'attribute', 'node': ANY},
    ]),

    ('<text><span class="test">{ markup }</span></text>', [
        {'expression': '<span class="test">{ markup }</span>', 'type': 'markup', 'node': ANY},
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
