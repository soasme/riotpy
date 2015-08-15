# -*- coding: utf-8 -*-

from pyquery import PyQuery

def convert_string_to_node(string):
    return PyQuery(string)
