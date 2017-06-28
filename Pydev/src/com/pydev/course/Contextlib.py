'''
Created on 2017年6月28日

@author: xusheng
'''

from contextlib import contextmanager, closing
from urllib.request import urlopen

class Query(object):
    def __init__(self, name):
        self.name = name

    def query(self):
        print('query info about [%s]' % self.name)

@contextmanager
def create_query(name):
    print('begin')
    q = Query(name)
    yield q
    print('end')

@contextmanager
def tag(name):
    print('<%s>' % name)
    yield
    print('</%s>' % name)

if __name__ == '__main__':
    with create_query('hello') as q:
        q.query()
    print()
    
    with tag('html'):
        with tag('body'):
            print('hello world')
    print()
    
    with closing(urlopen('http://www.python.org')) as page:
        for line in page:
            print(line)
