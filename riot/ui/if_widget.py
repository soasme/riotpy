# -*- coding: utf-8 -*-

import urwid

class IfWidget(urwid.WidgetDecoration):
    def __init__(self, if_widget, state=True):
        self.if_widget = if_widget
        self.solid_widget = urwid.SolidFill()
        self.state = state

    def _get_original_widget(self):
        if self.state:
            return self.if_widget
        else:
            return self.solid_widget

    def _set_original_widget(self, original_widget):
        self.if_widget = original_widget
        self._invalidate()

    original_widget = property(_get_original_widget, _set_original_widget)
    _original_widget = original_widget

    def rows(self, size, focus=False):
        if self.state:
            return self.if_widget.rows(size, focus)
        else:
            return 0

    def render(self, size, focus=False):
        if self.state:
            return self.if_widget.render(size, focus)
        else:
            col, = size
            return self.solid_widget.render((col, 0), focus)

    def show(self):
        self.state = True
        self._invalidate()

    def hide(self):
        self.state = False
        self._invalidate()

    def toggle(self):
        self.state = not self.state
        self._invalidate()


if __name__ == '__main__':
    showable = IfWidget(urwid.Text('hello world'))
    def handler(key):
        if key in ('q', 'Q'):
            raise urwid.ExitMainLoop()
        showable.toggle()
    filler = urwid.Filler(showable, 'top')
    loop = urwid.MainLoop(filler, unhandled_input=handler)
    loop.run()
