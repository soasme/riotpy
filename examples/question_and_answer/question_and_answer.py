# -*- coding: utf-8 -*-

from riot.app import quit_app, run_tag
from riot.tags.tags import parse_tag_from_node
from riot.tags.utils import convert_string_to_node
from riot.virtual_dom import define_tag, mount

question_box = define_tag('question-box', '''
<question-box>
  <filler keypress="{ keypress }">
    <edit caption="Who is your love?\n" />
  </filler>
  <script>
  def init(self, opts):
      self.name = opts['name']
      self.enable_input = True
  def keypress(self, size, key):
      import sys, urwid
      print >> sys.stderr, size, key
      if not self.enable_input:
          return True
      if key == 'enter':
          self.enable_input = True
          self.name = self.ui.body.edit_text
          self.ui.body = urwid.Text('%s loves you, too. Press q to exit.' % self.name)
          return True
      return False
  </script>
</question-box>
''')

root = convert_string_to_node('<question-box></question-box>')

mount(root, 'question-box', 'question-box', {'name': 'hello world'})

app = parse_tag_from_node(root)

run_tag(
    app,
    unhandled_input=lambda key: key in ('q', 'Q') and quit_app()
)
