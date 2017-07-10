'''
Created on 2017年6月23日

@author: xusheng
'''

import random, time, queue
from multiprocessing.managers import BaseManager

task_queue = queue.Queue()
result_queue = queue.Queue()

def get_task_queue():
    return task_queue

def get_result_queue():
    return result_queue

class TaskManager(BaseManager):
    pass
    
if __name__ == '__main__':
    TaskManager.register('get_task_queue', get_task_queue)
    TaskManager.register('get_result_queue', get_result_queue)

    server = '127.0.0.1'
    port = 5000
    
    qm = TaskManager(address=(server, port), authkey=b'authkey')
    qm.start()
     
    task = qm.get_task_queue()
    result = qm.get_result_queue()
     
    for i in range(20):
        n = random.randint(0, 10000)
        print('Put task %d...' % n)
        task.put(n)
 
    while True:
        try:
            r = result.get(timeout=3)
            print('Result: %s' % r)
        except queue.Empty as e:
            print('result queue is empty')
     
    qm.shutdown()
    print('task manager exit.')
