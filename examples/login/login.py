# -*- coding: utf-8 -*-

from riotpy import Observable, riot_open

auth = Observable('auth')

@auth.callable
def login(username, password):
    if username == 'admin' and password == 'password':
        auth.trigger('login.success', {'id': 1, 'username': 'admin'})
    else:
        auth.trigger('login.fail', {'msg': u'Wrong password'})

if __name__ == '__main__':
    riot_open('./index.tag', auth)
