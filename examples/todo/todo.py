# -*- coding: utf-8 -*-

from riot.app import quit_app, run_tag
from riot.tags.style import parse_style
from riot.tags.tags import parse_tag_from_node
from riot.tags.utils import convert_string_to_node
from riot.virtual_dom import define_tag, mount

todo = define_tag('todo', '''<todo>
  <pile>
    <text>{ title }</text>
    <checkbox label="{ title }" state="{ done }" onchange="{ check }" each="{ items }"></checkbox>
    <edit name="input"></edit>
    <button label="Add #{ next_count() }" onclick="{ add }" />
    <button label="Remove done" onclick="{ remove_all_done }" />
    <button label="Exit" onclick="{ exit }" />
  </pile>
  <script>
    def init(self, opts):
        self.items = opts['items']
        self.title = opts['title']


    def check(self, e):
        index = e.target.loopindex
        item = self.items[index]
        item['done'] = e.data['state']

    def add(self, e):
        input = self.el("edit[name=input]")
        text = input.edit_text
        if not text:
            return
        self.items = self.items + [dict(title=text, done=False, hidden=False)]
        input.edit_text = ''

    def remove_all_done(self, e):
        self.items = [item for item in self.items if not item.get('done')]

    def not_hidden_items(self):
        return [item for item in self.items if not item.get('hidden')]

    def count(self):
        return len(self.items)

    def next_count(self):
        return self.count() + 1

    def toggle(self, e):
        e.item['done'] = not e.item.get('done')
        return True
  </script>
</todo>''')


root = convert_string_to_node('<filler><todo></todo></filler>')

mount(root, 'todo', 'todo', {
    'title': 'TODO list',
    'items': [
        {'title': 'Avoid excessive coffeine', 'done': True, 'hidden': False},
        {'title': 'Hidden item', 'done': True, 'hidden': True},
        {'title': 'Be less provocative', 'done': False, 'hidden': False},
        {'title': 'Be nice to people', 'done': False, 'hidden': False}
    ]
})

app = parse_tag_from_node(root)

run_tag(app)
