'''
Created on Jun 10, 2017

@author: xusheng
'''

#coding=utf-8

import urllib.request

def getHtml():
    u = 'http://s7d9.scene7.com/is/image/GenuinePartsCompany/'
    
    cat = range(1, 2)
    #18
    sub = range(1, 2)
    #16
    
    for i in cat:
        for j in sub:
            url = u + 'cat' + str(i) + 'sub' + str(j) + '?$NOL%20Sub%20Cat$'
            print(url)
            req = urllib.request.urlopen(url)
            buf = req.read()
            f = open('/Users/xusheng/Desktop/temp/' + str(i) + '-' + str(j) + '.jpg', 'wb')
            f.write(buf)
        
        

if __name__ == '__main__':
    getHtml()