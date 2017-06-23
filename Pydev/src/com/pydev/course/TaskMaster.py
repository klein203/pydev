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

class QueueManager(BaseManager):
    pass
#     _task_queue = queue.Queue()
#     _result_queue = queue.Queue()
#     
#     @property
#     def task_queue(self):
#         return self._task_queue
# 
#     @property
#     def result_queue(self):
#         return self._result_queue
    
if __name__ == '__main__':
#     print('QueueManager.task_queue: type %s, obj %s' % (type(QueueManager.task_queue), QueueManager.task_queue))
#     print('QueueManager.result_queue: type %s, obj %s' % (type(QueueManager.result_queue), QueueManager.result_queue))
#     print('QueueManager._task_queue: type %s, obj %s' % (type(QueueManager._task_queue), QueueManager._task_queue))
#     print('QueueManager._result_queue: type %s, obj %s' % (type(QueueManager._result_queue), QueueManager._result_queue))
    
#     QueueManager.register('get_task_queue', QueueManager.task_queue)
#     QueueManager.register('get_result_queue', QueueManager.result_queue)

    QueueManager.register('get_task_queue', get_task_queue)
    QueueManager.register('get_result_queue', get_result_queue)

    qm = QueueManager(address=('127.0.0.1', 5000), authkey=b'authkey')
    qm.start()
     
    task = qm.get_task_queue()
    result = qm.get_result_queue()
     
    for i in range(10):
        n = random.randint(0, 10000)
        print('Put task %d...' % n)
        task.put(n)
 
    print('Try to get results...')
    for i in range(10):
        r = result.get(timeout=10)
        print('Result: %s' % r)
     
    qm.shutdown()
    print('master exit.')
