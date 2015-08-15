# -*- coding: utf-8 -*-

from urwid import Text
from pyquery import PyQuery

def parse_tag_from_string(string):
    return parse_tag_from_node(convert_string_to_node(string))

def parse_tag_from_node(node):
    return Text(node.text())

def convert_string_to_node(string):
    return PyQuery(string)
