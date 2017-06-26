'''
Created on 2017年6月26日

@author: xusheng
'''

from collections import namedtuple, deque, defaultdict, OrderedDict, Counter

if __name__ == '__main__':
    Point = namedtuple('Point', ['x', 'y'])
    p = Point(1, 2)
    print('namedtuple Point p =', p)
    
    Circle = namedtuple('Circle', ['x', 'y', 'r'])
    c = Circle(1, 1, 3)
    print('namedtuple Circle c =', c)
    
    
    q = deque(['a', 'b', 'c'])
    print('init q = %s' % q)
    q.appendleft('x')
    q.append('y')
    print('after append = %s' % q)
    q.pop()
    print('after pop = %s' % q)
    
    dd = defaultdict(lambda: 'N/A')
    dd['key1'] = 'val1'
    print('dd[key1] = %s' % dd['key1'])
    print('dd[key2] = %s' % dd['key2'])
    
    d = dict([('k4', 'v1'), ('k2', 'v2'), ('k3', 'v3')])
    print('d = %s' % d)
    od = OrderedDict([('k1', 'v1'), ('k2', 'v2'), ('k3', 'v3')])
    print('od = %s' % od)
    
    c = Counter()
    for ch in 'programming':
        c[ch] = c[ch] + 1
    print('counter word \'programming\' = %s' % c)
