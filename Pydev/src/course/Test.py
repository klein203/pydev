'''
Created on 2017��6��21��

@author: xusheng
'''

import logging
import pickle



def catchexpection():
    def foo(s):
        return 10 / int(s)

    def bar(s):
        return foo(s) * 2
    
    try:
        bar('0')
    except Exception as e:
        logging.exception(e)
    finally:
        print('finally...')

def withfile():
    with open('d:\\tmp\\1-1.jpg', 'br') as fi:
        buf = fi.read()
        with open('d:\\tmp\\1-1-backup.jpg', 'bw') as fo:
            fo.write(buf)

def dumpfile():
    with open('d:\\tmp\\1-1.jpg', 'br') as fi:
        buf = fi.read()
        with open('d:\\tmp\\1-1.dump', 'bw') as fo:
            pickle.dump(buf, fo)

def restorefile():
    with open('d:\\tmp\\1-1.dump', 'br') as fi:
        d = pickle.load(fi)
        with open('d:\\tmp\\1-1-restore.jpg', 'bw') as fo:
            fo.write(d)
    

if __name__ == '__main__':
    dumpfile()
    restorefile()
        