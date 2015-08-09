# -*- coding: utf-8 -*-

from riotpy import Observable, Riot

auth = Observable('auth')

@auth.callable
def login(username, password):
    if username == 'admin' and password == 'password':
        auth.trigger('login.success', {'id': 1, 'username': 'admin'})
    else:
        auth.trigger('login.fail', {'msg': u'Wrong password'})

app = Riot(__name__, './index.tag')
app.mount('login', auth)

if __name__ == '__main__':
    app.run(debug=True)
