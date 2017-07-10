'''
Created on 2017年6月27日

@author: xusheng
'''

import hashlib

def md5digest():
    s = 'how to use md5 in python hashlib?'
    md5 = hashlib.md5()
    md5.update(s.encode('utf-8'))
    print('md5[%s] = %s' % (s, md5.hexdigest()))

def sha1digest():
    s = 'how to use sha1 in python hashlib?'
    s1 = 'how to use sha1 '
    s2 = 'in python hashlib?'
    sha1 = hashlib.sha1()
    sha1.update(s.encode('utf-8'))
    print('sha1[%s] = %s' % (s, sha1.hexdigest()))
    
    sha2 = hashlib.sha1()
    sha2.update(s1.encode('utf-8'))
    sha2.update(s2.encode('utf-8'))
    print('sha1[%s] = %s' % (s, sha2.hexdigest()))
    
if __name__ == '__main__':
    md5digest()
    sha1digest()