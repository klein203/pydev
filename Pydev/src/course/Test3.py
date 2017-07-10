'''
Created on Jun 10, 2017

@author: xusheng
'''

#coding=utf-8

import urllib.request

def getHtml(url):
    req = urllib.request.urlopen(url)
    data = req.read()
    data = data.decode('UTF-8')
    return data

def saveFile(file, buf, mode = 'w', encoding = 'UTF-8'):
    with open(file, mode, 10240, encoding) as f:
        f.write(buf)

if __name__ == '__main__':
#     url = 'http://cn.bing.com/'
    url = 'http://www.baidu.com/s?'
    d = dict([['word', 'hello world!']])
    word = urllib.parse.urlencode(d)
    print(word)
    full_url = url + word
    
    path = '/Users/xusheng/Desktop/temp/'
    file = path + 'test.txt'

    content = getHtml(full_url)
#     print(content)
#     saveFile(file, content, 'w')
    