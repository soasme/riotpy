# -*- coding: utf-8 -*-

import urwid

def run_tag(tag, *args, **kwargs):
    loop = urwid.MainLoop(tag, *args, **kwargs)
    loop.screen.set_terminal_properties(colors=256)
    loop.run()

def quit_app():
    raise urwid.ExitMainLoop()
