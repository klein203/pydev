'''
Created on 2017年6月27日

@author: xusheng
'''
import struct

def int2bytes():
    n = 10240099
    b1 = (n & 0xff000000) >> 24
    b2 = (n & 0xff0000) >> 16
    b3 = (n & 0xff00) >> 8
    b4 = n & 0xff
    bs = bytes([b1, b2, b3, b4])
#     for i in bs:
#         print(i)
    print(bs)

def pack():
    print('pack >I 10240099 = %s' % struct.pack('>I', 10240099))
    print('pack >H (10240099 & 0xffff0000) >> 16 = %s' % struct.pack('>H', (10240099 & 0xffff0000) >> 16))
    print('pack >H (10240099 & 0xffff) = %s' % struct.pack('>H', (10240099 & 0xffff)))

def unpack():
    s = b'\xf0\xf0\xf0\xf0\x80\x80'
    print('unpack >IH', s, '=', struct.unpack('>IH', s))
    
#     BMP格式采用小端方式存储数据，文件头的结构按顺序如下：
#     两个字节：'BM'表示Windows位图，'BA'表示OS/2位图；
#     一个4字节整数：表示位图大小；
#     一个4字节整数：保留位，始终为0；
#     一个4字节整数：实际图像的偏移量；
#     一个4字节整数：Header的字节数；
#     一个4字节整数：图像宽度；
#     一个4字节整数：图像高度；
#     一个2字节整数：始终为1；
#     一个2字节整数：颜色数。
    bmp = b'\x42\x4d\x38\x8c\x0a\x00\x00\x00\x00\x00\x36\x00\x00\x00\x28\x00\x00\x00\x80\x02\x00\x00\x68\x01\x00\x00\x01\x00\x18\x00'
    print('unpack <ccIIIIIIHH', bmp, '=', struct.unpack('<ccIIIIIIHH', bmp))
    
    
if __name__ == '__main__':
#     int2bytes()
#     pack()
    unpack()
    