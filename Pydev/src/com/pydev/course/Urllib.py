'''
Created on 2017年6月28日

@author: xusheng
'''

from urllib import request

def openurl():
    url = 'https://api.douban.com/v2/book/2129650'    
#     url = 'http://www.chexiang.com'

    with request.urlopen(url) as f:
        data = f.read()
        print('request status = [%s][%s]' % (f.status, f.reason))
    
    #header
    for k, v in f.getheaders():
        print('%s = [%s]' % (k, v))
    print('Data =', data.decode('utf-8'))

def openreq():
    url = 'http://www.douban.com'
    req = request.Request(url)
    req.add_header('User-Agent', 'Mozilla/6.0 (iPhone; CPU iPhone OS 8_0 like Mac OS X) AppleWebKit/536.26 (KHTML, like Gecko) Version/8.0 Mobile/10A5376e Safari/8536.25')

    with request.urlopen(req) as f:
        data = f.read()
        print('request status = [%s][%s]' % (f.status, f.reason))
    
    #header
    for k, v in f.getheaders():
        print('%s = [%s]' % (k, v))
    print('Data =', data.decode('utf-8'))


if __name__ == '__main__':
    openreq()
    
