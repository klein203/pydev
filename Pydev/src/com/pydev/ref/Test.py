#!/usr/bin/env python3
# -*- coding: utf-8 -*-
'''
Created on May 25, 2017

@author: xusheng
'''
import math
from functools import reduce
import functools
# from PIL import Image

def normalize(name):
    return name.capitalize()

def c1():
    a = input("please type word:")
    L1 = [a, 'b', 'c']
    L2 = list(map(normalize, L1))
    print(L2)

def c2():
    print(ord('中'))
    print(ord('a'))
    print(chr(100))
    print(chr(30000))

def c3():
    print('ABC'.encode(encoding='ascii', errors='strict'))
    print('中文'.encode(encoding='utf-8', errors='strict'))
    print('中文'.encode(encoding='gb2312', errors='strict'))
    print('中文'.encode(encoding='gbk', errors='strict'))
#     print('中文'.encode(encoding='ascii', errors='strict'))

def c4():
    print('%03d, %.2f%%, %s, 0x%x' % (10, 1.4, 'abc', 123))
#     小明成绩
    s1 = 72
    s2 = 85
    r = (s2 - s1) * 100 / s1
    print('%2.1f%%' % r)

def c5():
    L = [
    ['Apple', 'Google', 'Microsoft'],
    ['Java', 'Python', 'Ruby', 'PHP'],
    ['Adam', 'Bart', 'Lisa']
    ]
    for item in L:
        for unit in item:
            print(unit)

def c6():
#     s = set([2, 3, 4])
    s = {2, 3, 4}
    s.add(1)
    s.remove(3)
    print('s =', s)
    
#     d = {['a', 2], ['b', 3], ['c', 4]}
    d = dict([['a', 2], ['b', 3], ['c', 4]])
    for key in d.keys():
        print('key = %s, value = %s' % (key, d[key]))
    print('d =', d)         

def c7():
    # f(x) = ax^2 + bx + c
    def quadratic(a, b, c):
        for i in [a, b, c]:
            if not isinstance(i, (int, float)):
                raise TypeError('bad operand type', i)
        return ((-b + math.sqrt((b ** 2 - 4 * a * c))) / (2 * a), (-b - math.sqrt((b ** 2 - 4 * a * c))) / (2 * a))
    print(quadratic(2, 3, 1))
    print(quadratic(1, 3, -4))

def sumall(*numbers):
    s = 0
    for n in numbers:
        s = s + n
    return (s)

def c8():
    v = [1, 2, 3, 4, 5]
    print(sumall(*v))

def f1(a, b, c = 0, *args, **kw):
    print('a =', a, 'b =', b, 'c =', c, 'args =', args, 'kw =', kw)

def c5_2():
    def hanoimove(n, a, b, c):
        if n == 1:
            print(a, '-->', c)
        else:
            hanoimove(n-1, a, c, b)
            hanoimove(1, a, b, c)
            hanoimove(n-1, b, a, c)
    hanoimove(3, 'A', 'B', "C")

def c5_3():
    L = ['Hello', 'World', 18, 'Apple', None]
    print([s.lower() for s in L if isinstance(s, str)])

def odd(m):
    n = 0
    while n < m:
        if n % 2 == 1:
            yield(n)
            n = n + 2
        else:
            n = n + 1

def fibonacci(m):
    n, a, b = 0, 0, 1
    while n < m:
        yield(b)
        a, b = b, a + b
        n = n + 1

def c5_4():
    def yh_triangle(m):
        n, L = 0, []
        while n < m:
            if n == 0:
                L.append(1)
            else:
                L.append(0)
                L = [L[i-1] + L[i] for i in range(len(L))]
            yield(L)
            n = n + 1

    func = yh_triangle(10)
    for i in func:
        print(i)

def c6_1():
    def normalize(name):
        return name.capitalize()
    
    def prod(L):
        return reduce(lambda x, y: x * y, L)
    
    def str2float(s):
        dotIndex = s.find('.')
        s = s.replace('.', '')
        dotTimes = len(s) - dotIndex
        return reduce(lambda x, y: 10 * x + y, map(int, s)) / pow(10, dotTimes)
    
    L1 = ['adam', 'LISA', 'barT']
    L2 = list(map(normalize, L1))
    print(L2)
    
    print('3 * 5 * 7 * 9 =', prod([3, 5, 7, 9]))
    
    print('str2float(\'123.456\') =', str2float('123.456'))

def c6_2():
    def is_palindrome(n):
        return str(n) == str(n)[::-1] and len(str(n)) > 1
    
    output = filter(is_palindrome, range(1, 1000))
    print(list(output))

def c6_3():
    def by_name(t):
        return t[0]
    def by_score(t):
        return t[1]
    L = [('Bob', 75), ('Adam', 92), ('Bart', 66), ('Lisa', 88)]
    L2 = sorted(L, key = by_name)
    print(L2)
    L3 = sorted(L, key = by_score, reverse = True)
    print(L3)

def log(msg):
    def decoratorFactory(msg = ''):
        def decorator(f):
            @functools.wraps(f)
            def wrapper(*args, **kw):
                print('extra msg: %s' % msg)
                print("begin call %s()" % f.__name__)
                res = f(*args, **kw)
                print('end call %s(), return [%s]' % (f.__name__, res))
                return res
            return wrapper
        return decorator
    if isinstance(msg, str):
        return decoratorFactory(msg)
    else:
        return decoratorFactory()(msg)


def c6_6():
    @log
    def now():
        print('2017-5-31')
    now()

class Screen(object):
    @property
    def width(self):
        return self._width

    @width.setter
    def width(self, width):
        self._width = width

    @property
    def height(self):
        return self._height

    @height.setter
    def height(self, height):
        self._height = height
     
    @property
    def resolution(self):
        return self._width * self._height
    
def c9_2():
    s = Screen()
    s.width = 1024
    s.height = 768
    print(s.resolution)
    assert s.resolution == 786432, '1024 * 768 = %d ?' % s.resolution

if __name__ == '__main__':
    c9_2()
