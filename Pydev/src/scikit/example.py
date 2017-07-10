'''
Created on 2017年6月29日

@author: xusheng
'''

from numpy import *

def example():
    arr = random.rand(4, 4)
    ma = mat(arr)
    inv_ma = ma.I
    print('array =\n', arr)
    print('matrix =\n', ma)
    print('inv_matrix =\n', inv_ma)
    print('matrix * inv_matrix =\n', ma * inv_ma)
    print('matrix * inv_matrix - eye(4) =\n', ma * inv_ma - eye(4))

if __name__ == '__main__':
    example()
    