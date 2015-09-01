# -*- coding: utf-8 -*-

from riot.app import quit_app, run_tag
from riot.tags.style import parse_style
from riot.tags.tags import parse_tag_from_node
from riot.tags.utils import convert_string_to_node
from riot.virtual_dom import define_tag, mount

todo = define_tag('todo', '''<todo>
  <listbox>
    <text>{ title }</text>
    <checkbox label="{ title }" state="{ done }" each="{ items }" />
    <edit name="input" />
    <button label="Add #{ next_count() }" onclick="{ add }" />
    <button label="X" onclick="{ remove_all_done }" />
    <button label="Exit" onclick="{ exit }">
  </listbox>
  <script>
    def init(self, opts):
        self.items = opts['items']
        self.title = opts['title']

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

    def count(self):
        return len(self.not_hidden_items())

    def next_count(self):
        return self.count() + 1

    def toggle(self, e):
        e.item['done'] = not e.item.get('done')
        return True
  </script>
</todo>''')


root = convert_string_to_node('<filler><todo /></filler>')

mount(root, 'todo', 'todo', {
    'title': 'I want to behave!',
    'items': [
        {'title': 'Avoid excessive coffeine', 'done': True, 'hidden': False},
        {'title': 'Hidden item', 'done': True, 'hidden': True},
        {'title': 'Be less provocative', 'done': False, 'hidden': False},
        {'title': 'Be nice to people', 'done': False, 'hidden': False}
    ]
})

app = parse_tag_from_node(root)

run_tag(app)
