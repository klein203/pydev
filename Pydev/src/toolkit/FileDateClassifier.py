'''
Created on 2017年11月6日

@author: xusheng
'''
import os
import shutil
import datetime
import sys
import getopt

def process(srcPath, tarPath):
    filelist = os.listdir(srcPath)
    # if filelist is not empty
    if filelist:
        for file in filelist:
            filefullpathorname = os.path.join(srcPath, file)
            # if obj is dir, recursively dig directory
            if os.path.isdir(filefullpathorname):
                process(filefullpathorname, tarPath)
            # if obj is file
            elif os.path.isfile(filefullpathorname):
                # TODO
                moveFile(file, srcPath, tarPath)
    else:
        return 

def moveFile(file, srcPath, tarPath):
    filefullname = os.path.join(srcPath, file)
    date = datetime.datetime.fromtimestamp(os.path.getmtime(filefullname))
    datestr = date.strftime('%Y%m%d')
    
    targetfullpath = os.path.join(tarPath, datestr)
    
    # if not exist, create new directory
    if not os.path.exists(targetfullpath):
        os.mkdir(targetfullpath)
    
    targetfullname = os.path.join(targetfullpath, file)
    
    # just move file to the target path
    shutil.move(filefullname, targetfullname)
    print('move %s to %s' % (filefullname, targetfullname))

def usage():
    print('Usage: move files from source path to target path, make sure that both directories exists')
    print()
    print('CMD: python FileDateClassifier.py -s sourcepath -t targetpath')
    print()
    print('Parameter:')
    print('    -s: source path')
    print('    -t: target path')
    print('    -h: help')
    
    
if __name__ == '__main__':
    opts, args = getopt.getopt(sys.argv[1:], "hs:t:")
    for op, value in opts:
        if op == "-s":
            srcPath = value
        elif op == "-t":
            tarPath = value
        elif op == "-h":
            usage()
            sys.exit()
            
#     srcPath = 'd:\\tmp\\fdc'
#     tarPath = 'd:\\tmp\\fdc_tar'
    
    process(srcPath, tarPath)
    print('all done!')
    
