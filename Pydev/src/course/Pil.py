'''
Created on 2017年6月28日

@author: xusheng
'''

from PIL import Image, ImageFilter, ImageFont, ImageDraw
import random

def resize():
    im = Image.open('d:\\tmp\\1-1.jpg')
    w, h = im.size
    print('Original image size: %sx%s' % (w, h))
    im.thumbnail((w//2, h//2))
    print('Resize image to: %sx%s' % (w//2, h//2))
    im.save('d:\\tmp\\1-1-thumbnail.jpg', 'jpeg')

def blur():
    im = Image.open('d:\\tmp\\1-1.jpg')

    im2 = im.filter(ImageFilter.BLUR)
    im2.save('d:\\tmp\\1-1-blur.jpg', 'jpeg')

def rndChar():
    return chr(random.randint(65, 90))

def rndColor():
    return (random.randint(64, 255), random.randint(64, 255), random.randint(64, 255))

def rndColor2():
    return (random.randint(32, 127), random.randint(32, 127), random.randint(32, 127))

def rndCode():
    width, height = 60 * 4, 60    
    image = Image.new('RGB', (width, height), (255, 255, 255))
    
    font = ImageFont.truetype('C:\\Windows\\Fonts\\Arial.ttf', 36)
    
    draw = ImageDraw.Draw(image)
    
    for x in range(width):
        for y in range(height):
            draw.point((x, y), fill=rndColor())
    
    code = ''
    for t in range(4):
        c = rndChar()
        draw.text((60 * t + 10, 10), c, font=font, fill=rndColor2())
        code = code + c   
    
    image = image.filter(ImageFilter.BLUR)
    image.save(('d:\\tmp\\' + code.upper() + '.jpg'), 'jpeg')
    
if __name__ == '__main__':
    resize()
    blur()
    rndCode()
    