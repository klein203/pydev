'''
Created on 2017年6月26日

@author: xusheng
'''

import re

def match():
    re_pattern = re.compile(r'^\d{3}\-\d{3,8}$')
    if re_pattern.match('010-12345'):
        print('match')
    else:
        print('failed')

def split():
    for i in re.split(r'[\s\,\;]+', 'a, b ;   c; ;d'):
        print('[%s]' % i)
        
if __name__ == '__main__':
    match()
    print()
    split()