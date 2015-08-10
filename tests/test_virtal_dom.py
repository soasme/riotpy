# -*- coding: utf-8 -*-

def test_mount_tag_to_root():
    impl = {
        'name': 'tag',
        'layout': [
            ['text', {}, '{ opts.text }'],
        ],
        'logic': ''
    }
    opts = {}
    root = {}
    g = {}
    tag = mount_tag_to_root(g, root, impl, opts)
    assert g[tag['uuid']] # ref to a ui library instance
    assert tag == {
        'uuid': ANY,
        'self': ANY, # an observable object, logic mount to self
        'impl': impl,
        'opts': opts, # an observable object
        'root': root,
        'parent': None,
        'tags': [
            {
                'uuid': ANY,
                'self': ANY,
                'impl': ANY, # built-in impl
                'opts': opts,
                'root': root,
                'parent': tag,
                'tags': []
            }
        ],
    }
    assert g[tag['tags'][0]] # ref to ui library text instance
