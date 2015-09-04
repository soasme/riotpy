# -*- coding: utf-8 -*-

import json
import urwid
import inspect
from functools import wraps
from riot.multimethods import MultiMethod, method

def boolean_filter(value):
    if value in ('off', 'False', 'None', '', None):
        return False
    return True

def integer_filter(value):
    return int(value)

def generate_widget_dispatch(document):
    return ("'%s'" % document[0].tag, )

generate_widget = MultiMethod('generate_widget', generate_widget_dispatch)

CACHE = {}

def cache_widget(f):
    @wraps(f)
    def _cache_widget(document):
        if not document.attr['data-riot-dirty'] and document.attr['data-riot-widget']:
            key = int(document.attr['data-riot-widget'])
            return CACHE[key]

        if document.attr['data-riot-widget']:
            key = int(document.attr['data-riot-widget'])
            del CACHE[key]

        widget = f(document)
        key = id(widget)
        CACHE[key] = widget
        document.attr['data-riot-widget'] = str(key)
        document.removeAttr('data-riot-dirty')
        return widget
    return _cache_widget

def generate_general_widget(document):
    tag = document[0].tag
    widget_classname = ''.join([t.capitalize() for t in tag.split('-')])
    widget_class = getattr(urwid, widget_classname)
    args = inspect.getargspec(widget_class.__init__).args
    args.remove('self')
    attr_args = {}
    for attribute, val in document[0].attrib.items():
        if attribute in args:
            attr_args[attribute] = val
    return widget_class, attr_args

@method("text")
@cache_widget
def generate_widget(document):
    widget_class, attr_args = generate_general_widget(document)
    attr_args['markup'] = json.loads(attr_args.get('markup') or '""')
    return widget_class(**attr_args)

@method('edit')
@cache_widget
def generate_widget(document):
    widget_class, attr_args = generate_general_widget(document)
    attr_args['multiline'] = boolean_filter(attr_args.get('multiline'))
    attr_args['allow_tab'] = boolean_filter(attr_args.get('allow_tab'))
    if 'edit_pos' in attr_args:
        attr_args['edit_pos'] = int(attr_args['edit_pos'])
    return widget_class(**attr_args)

@method('check-box')
@cache_widget
def generate_widget(document):
    widget_class, attr_args = generate_general_widget(document)
    attr_args['state'] = boolean_filter(attr_args.get('state'))
    return widget_class(**attr_args)

@method('attr-map')
@cache_widget
def generate_widget(document):
    assert document.children() and len(document.children()) == 1
    widget_class, attr_args = generate_general_widget(document)
    child = document.children().eq(0)
    attr_args['w'] = generate_widget(child)
    return widget_class(**attr_args)

@method('padding')
@cache_widget
def generate_widget(document):
    assert document.children() and len(document.children()) == 1
    widget_class, attr_args = generate_general_widget(document)
    child = document.children().eq(0)
    attr_args['w'] = generate_widget(child)
    attr_args['left'] = int(attr_args.get('left') or 0)
    attr_args['right'] = int(attr_args.get('right') or 0)
    return widget_class(**attr_args)

@method('filler')
@cache_widget
def generate_widget(document):
    assert document.children() and len(document.children()) == 1
    widget_class, attr_args = generate_general_widget(document)
    child = document.children().eq(0)
    attr_args['w'] = generate_widget(child)
    attr_args['top'] = int(attr_args.get('top') or 0)
    attr_args['bottom'] = int(attr_args.get('bottom') or 0)
    return widget_class(**attr_args)

@method('divider')
@cache_widget
def generate_widget(document):
    widget_class, attr_args = generate_general_widget(document)
    attr_args['top'] = int(attr_args.get('top') or 0)
    attr_args['bottom'] = int(attr_args.get('bottom') or 0)
    attr_args['div_char'] = attr_args.get('div_char') or ' '
    return widget_class(**attr_args)

@method('line-box')
@cache_widget
def generate_widget(document):
    assert document.children() and len(document.children()) == 1
    widget_class, attr_args = generate_general_widget(document)
    child = document.children().eq(0)
    attr_args['original_widget'] = generate_widget(child)
    return widget_class(**attr_args)

@method('solid-fill')
@cache_widget
def generate_widget(document):
    widget_class, attr_args = generate_general_widget(document)
    return widget_class(**attr_args)

@method('pop-up-launcher')
@cache_widget
def generate_widget(document):
    widget_class, attr_args = generate_general_widget(document)
    return widget_class(**attr_args)

@method('frame')
@cache_widget
def generate_widget(document):
    widget_class, attr_args = generate_general_widget(document)
    body = document.children('body')
    assert body
    assert len(body.children()) == 1
    attr_args['body'] = generate_widget(body.children())
    header = document.children('header')
    if header:
        assert len(header.children()) == 1
        attr_args['header'] = generate_widget(header.children())
    footer = document.children('footer')
    if footer:
        assert len(footer.children()) == 1
        attr_args['footer'] = generate_widget(footer.children())
    return widget_class(**attr_args)

@method('list-box')
@cache_widget
def generate_widget(document):
    widget_class, attr_args = generate_general_widget(document)
    widgets = [generate_widget(child) for child in document.children()]
    walker = urwid.SimpleListWalker(widgets)
    attr_args['body'] = walker
    return widget_class(**attr_args)

@method('pile')
@cache_widget
def generate_widget(document):
    widget_class, attr_args = generate_general_widget(document)
    attr_args['focus_item'] = int(attr_args.get('focus_item') or 0)
    attr_args['widget_list'] = [generate_widget(child) for child in document.children()]
    return widget_class(**attr_args)
