'''
Created on 2017年6月27日

@author: xusheng
'''

import itertools

def iterfunc():
    cnt = 5
    natuals = itertools.count(1)
    print(type(natuals))
    for n in natuals:
        if cnt == 0:
            break
        cnt = cnt - 1
        print(n)
    print()
    
    cnt = 5
    cs = itertools.cycle('abc')
    for n in cs:        
        if cnt == 0:
            break
        cnt = cnt - 1
        print(n)
    print()
    
    cnt = 5
    ns = itertools.repeat('abc', 3)
    for n in ns:        
        if cnt == 0:
            break
        cnt = cnt - 1
        print(n)
    print()
    
    for n in itertools.chain('abc', 'xyz'):
        print(n)
    print()
    
    for key, group in itertools.groupby('AaaBBbcCAAa', lambda c: c.upper()):
        print(key, list(group))
    
    

if __name__ == '__main__':
    iterfunc()
