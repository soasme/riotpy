# -*- coding: utf-8 -*-

from pyquery import PyQuery
from riot.virtual_dom import define_tag, mount
from riot.observable import Observable
import re
import types

def fn(self, opts):
    cmd = ('''
def init(self, opts):
    self.items = opts.items

def edit(self, e):
    self.text = e.target.value

def add(self, e):
    if self.text:
        self.items.append(dict(title=self.text, done=False, hidden=False))
        self.text = self.input.value = ''

def remove_all_done(self, e):
    self.items = [item for item in self.items if not item.get('done')]

def not_hidden_items(self):
    return [item for item in self.items if not item.get('hidden')]

def toggle(self, e):
    e.item['done'] = not e.item.get('done')
    return True
    ''')
    exec cmd
    fnnames = re.findall(r'^def ([a-zA-Z0-9_]+)', cmd, re.MULTILINE)
    localfns = locals()
    fns = [localfns[fnname] for fnname in fnnames]
    for fnname in fnnames:
        attribute = types.MethodType(localfns[fnname], self, Observable)
        setattr(self, fnname, attribute)
    if hasattr(self, 'init'):
        self.init(opts)


tag = {
    'name': 'todo',
    'html': '''<todo>
  <text>{ opts.title }</text>
  <listbox>
    <each list="{ filter(not_hidden, self.items) }">
      <checkbox label="{ title }" state="{ completed }" on_state_change="{ parent.toggle }" />
    </each>
  </listbox>
  <edit name="input" />
  <button label="Add #{ len(filter(what_show, self.items) + 1 }" />
  <button label="X{ len(filter(only_done, self.items) }" on_press="{ remove_all_done }" />
  <script>
    def init(self, opts):
        self.items = opts.items

    def edit(self, e):
        self.text = e.target.value

    def add(self, e):
        if self.text:
            self.items.append(dict(title=self.text, done=False, hidden=False))
            self.text = self.input.value = ''

    def remove_all_done(self, e):
        self.items = [item for item in self.items if not item.get('done')]

    def not_hidden_items(self):
        return [item for item in self.items if not item.get('hidden')]

    def toggle(self, e):
        e.item['done'] = not e.item.get('done')
        return True
  </script>
</todo>''',
    'fn': fn,
}

define_tag(**tag)

root = PyQuery('<filler><todo></todo></filler>')

doms = mount(root, 'todo', 'todo', {
    'title': 'I want to behave!',
    'items': [
        {'title': 'Avoid excessive coffeine', 'done': True, 'hidden': False},
        {'title': 'Hidden item', 'done': True, 'hidden': True},
        {'title': 'Be less provocative', 'done': False, 'hidden': False},
        {'title': 'Be nice to people', 'done': False, 'hidden': False}
    ]
})
print vars(doms[0])
