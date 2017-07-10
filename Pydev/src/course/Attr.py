'''
Created on 2017年6月23日

@author: xusheng
'''

class Test(object):
    var = 1
    _var = 2
    __var = 3
    
    def __init__(self):
        self.var = 4
        self._var = 5
        self.__var = 6
        
    def print_var(self):
        print('-------------------------------------------')
        print('class.var is %s' % Test.var)
        print('class._var is %s' % Test._var)
        print('class.__var is %s' % Test.__var)
        print('instance.var is %s' % self.var)
        print('instance._var is %s' % self._var)
        print('instance.__var is %s' % self.__var)
        print('-------------------------------------------')

if __name__ == '__main__':
    print(dir(Test))
    
    inst = Test()
    print(dir(inst))
    inst.print_var()
    
    inst.var = 11
    inst._var = 12    
    inst.__var = 13
    Test.var = 14
    Test._var = 15
    Test.__var = 16
    print(dir(inst))
    inst.print_var()
    
    print(dir(Test))
    
