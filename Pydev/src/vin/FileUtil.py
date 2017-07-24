'''
Created on 2017年7月14日

@author: xusheng
'''

import pickle

def store(obj, filename):
    fw = open(filename, 'wb')
    pickle.dump(obj, fw)
    fw.close()
    
def load(filename):
    fr = open(filename, 'rb')
    return pickle.load(fr)
