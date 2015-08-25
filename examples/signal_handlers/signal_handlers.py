# -*- coding: utf-8 -*-

from riot.app import quit_app, run_tag
from riot.tags.style import parse_style
from riot.tags.tags import parse_tag_from_node
from riot.tags.utils import convert_string_to_node
from riot.virtual_dom import define_tag, mount

sig = define_tag('sig', '''
<sig>
  <filler valign="top">
    <pile>
      <edit caption="What is your name?" class="highlight" id="ask" onchange="{ answer }" />
      <div />
      <text><span if="{ name }">Nick to meet you, </span><span class="highlight">{ name }</span></text>
      <div />
      <button id="exit" label="Exit" onclick="{ exit }" />
    </pile>
  </filler>
  <script>
  import urwid

  def init(self, opts):
      import urwid
      self.name = opts['name']

  def answer(self, edit, text):
      self.update({'name': text})

  def exit(self, button):
      import urwid
      raise urwid.ExitMainLoop()



  </script>
</sig>
''')

style = '''
.highlight {
  foreground: default,bold;
  background: default;
  mono: bold;
}
'''

root = convert_string_to_node('<sig></sig>')

mount(root, 'sig', 'sig', {'name': 'Default'})

app = parse_tag_from_node(root)

run_tag(app, parse_style(style))
