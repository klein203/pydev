'''
Created on 2017年6月28日

@author: xusheng
'''

from xml.parsers.expat import ParserCreate

class DefaultSaxHandler(object):
    def start_element(self, name, attrs):
        print('sax:start_element: %s, attrs: %s' % (name, str(attrs)))
        
    def end_element(self, name):
        print('sax:end_element: %s' % name)

    def char_data(self, text):
        print('sax:char_data: %s' % text)

class ShiftSaxHandler(DefaultSaxHandler):
    shift = 0
    shift_ch = ' '
    
    def shiftch(self):
        n = self.shift
        sh = ''
        while n > 0:
            sh = sh + self.shift_ch
            n = n - 1
        return sh
        
    def start_element(self, name, attrs):
        print('%ssax:start_element: %s, attrs: %s' % (self.shiftch(), name, str(attrs)))
        self.shift = self.shift + 1
        
    def end_element(self, name):
        print('%ssax:end_element: %s' % (self.shiftch(), name))
        self.shift = self.shift - 1

    def char_data(self, text):
        print('%ssax:char_data: %s' % (self.shiftch(), text.strip()))
    

if __name__ == '__main__':
    xml = r'''<?xml version="1.0"?>
    <ol>
        <li><a href="/python">Python</a></li>
        <li><a href="/ruby">Ruby</a></li>
    </ol>
    '''
    
#     handler = DefaultSaxHandler()
    handler = ShiftSaxHandler()
    parser = ParserCreate()
    parser.StartElementHandler = handler.start_element
    parser.EndElementHandler = handler.end_element
    parser.CharacterDataHandler = handler.char_data
    parser.Parse(xml)