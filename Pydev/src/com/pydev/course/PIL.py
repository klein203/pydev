'''
Created on 2017年6月28日

@author: xusheng
'''

from PIL import Image

def resize():
    im = Image.open('d:\tmp\1-1.jpg')
    w, h = im.size
    print('Original image size: %sx%s' % (w, h))
    im.thumbnail((w//2, h//2))
    print('Resize image to: %sx%s' % (w//2, h//2))
    im.save('d:\tmp\1-1-thumbnail.jpg', 'jpeg')

if __name__ == '__main__':
    resize()
    