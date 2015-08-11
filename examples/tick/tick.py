# -*- coding: utf-8 -*-

from riotpy import Observable, Riot

app = Riot(__name__, './index.tag')
app.mount('tick')

if __name__ == '__main__':
    app.run(debug=True)

