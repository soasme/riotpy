# -*- coding: utf-8 -*-

def parse_style(string):
    styles_string = string.replace('\n', '')
    styles_string = styles_string.replace('}', '}\n')
    styles_lines = styles_string.split('\n')
    styles_lines = [_.strip() for _ in styles_lines if _.strip()]
    styles = []
    for style_line in styles_lines:
        assert style_line.startswith('.'), 'Only support class selector.'
        style_name = style_line[1:style_line.index('{')].strip()
        rules = style_line[style_line.index('{') + 1:-1]
        rules = [rule.strip().replace(';', '').split(':') for rule in rules.split(';')]
        rules = [rule for rule in rules if rule and len(rule) == 2]
        rules = {k.strip(): v.strip() for k, v in rules}
        foreground = rules.get('foreground', 'default')
        background = rules.get('background', 'default')
        mono = rules.get('mono')
        foreground_high = rules.get('foreground-height')
        background_high = rules.get('background-height')
        styles.append((style_name, foreground, background, mono, foreground_high, background_high))
    return styles
