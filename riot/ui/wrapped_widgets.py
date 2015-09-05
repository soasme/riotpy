# -*- coding: utf-8 -*-

from collections import namedtuple
from urwid import CheckBox, signals

class Event(namedtuple('Event', [
        'type',
        'target',
        'data',
])):
    pass

class Checkbox(CheckBox):

    def _emit(self, event, state):
        signals.emit_signal(self, event, Event(type=event, target=self, data={'state': state}))
