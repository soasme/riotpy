# -*- coding: utf-8 -*-

def walk(root, function, path=None):
    if not root:
        return
    path = path or []
    if not function(root, path):
        return
    for index, child in enumerate(root.children().items()):
        walk(child, function, path + [index])

def get_ui_by_path(root, path):
    import urwid
    ui = root
    for level in path:
        if level == 0:
            if isinstance(ui, urwid.Filler):
                ui = ui.body
            elif isinstance(ui, urwid.Pile):
                continue
            else:
                raise NotImplementedError(ui)
        else:
            ui = ui.contents[level][0]
    return ui
