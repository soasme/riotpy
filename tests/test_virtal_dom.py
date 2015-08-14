# -*- coding: utf-8 -*-

def test_mount_tag():
    pass

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
    g = {'instances': {}, 'attrs': {}}
    tag = mount_tag_to_root(g, impl, opts)
    assert g['instances'][tag['uuid']] # ref to a ui library instance
    assert tag == {
        'uuid': ANY,
        'impl': impl,
        'opts': opts,
        'root': root,
        'parent': None,
        'tags': [
            {
                'uuid': ANY,
                'impl': ANY, # built-in impl
                'opts': opts,
                'root': root,
                'parent': tag,
                'tags': []
            }
        ],
    }
    assert g['instances'][tag['tags'][0]] # ref to ui library text instance

