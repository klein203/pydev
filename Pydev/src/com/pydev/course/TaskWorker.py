'''
Created on 2017年6月23日

@author: xusheng
'''
import time, sys, queue
from multiprocessing.managers import BaseManager

class TaskWorker(BaseManager):
    pass

if __name__ == '__main__':
    TaskWorker.register('get_task_queue')
    TaskWorker.register('get_result_queue')
    
    server = '127.0.0.1'
    port = 5000
    
    print('Connect to server %s:%s...' % (server, port))
    qm = TaskWorker(address=(server, port), authkey=b'authkey')
    qm.connect()
    
    task_queue = qm.get_task_queue()
    result_queue = qm.get_result_queue()
    
    while True:
        try:
            n = task_queue.get(timeout=1)
            print('run task %d * %d...' % (n, n))
            r = '%d * %d = %d' % (n, n, n*n)
            time.sleep(1)
            result_queue.put(r)
        except queue.Empty as e:
            print('task queue is empty.')
            break

    print('task worker exit.')