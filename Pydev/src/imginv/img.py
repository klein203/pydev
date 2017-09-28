'''
Created on 2017年9月19日

@author: xusheng
'''
import numpy as np
import tensorflow as tf
import imginv.img_input as ip

BATCH_SIZE = 1

# def placeholder_inputs(batch_size):
#     images_placeholder = tf.placeholder(tf.float32, shape=[batch_size, IMG_WIDTH_PIXEL, IMG_HEIGHT_PIXEL, IMG_CHANNEL], name='image_pl')
#     return images_placeholder
    
def inference(image, dtype='origin'):
#     x = tf.constant(image, dtype=tf.float32, name='x')
    if dtype == 'origin':
        k = np.zeros([3, 3, 3, 3])
        k[1, 1, :, :] = 1
    elif dtype == 'sharpen':
        k = np.zeros([3, 3, 3, 3])
        k[0, 1, :, :] = -1
        k[2, 1, :, :] = -1
        k[1, 0, :, :] = -1
        k[1, 2, :, :] = -1
        k[1, 1, :, :] = 5
    elif dtype == 'edge':
        k = np.ones([3, 3, 3, 3]) * -1
        k[1, 1, :, :] = 8
    elif dtype == 'boxblur':
        k = np.ones([3, 3, 3, 3]) / 9.
    elif dtype == 'gaussblur':
        k = np.ones([3, 3, 3, 3]) / 16.
        k[0, 1, :, :] = 2. / 16.
        k[2, 1, :, :] = 2. / 16.
        k[1, 0, :, :] = 2. / 16.
        k[1, 2, :, :] = 2. / 16.
        k[1, 1, :, :] = 4. / 16.
    else: # default origin
        k = np.zeros([3, 3, 3, 3])
        k[1, 1, :, :] = 1

    w = tf.constant(k, dtype=tf.float32, name='w')
#     w = tf.Variable(initial_value=k, trainable=False, dtype=tf.float32, name='w')

    conv = tf.nn.conv2d(image, w, [1, 3, 3, 1], 'SAME', name='conv')
    tf.summary.image(('conv_op_%s' % dtype), conv)
    
    sigmoid = tf.sigmoid(conv, name='sig')
    tf.summary.image(('sig_op_%s' % dtype), sigmoid)
 
    maxpool = tf.nn.max_pool(sigmoid, [1, 3, 3, 1], [1, 3, 3, 1], 'SAME', name='pool')
    tf.summary.image(('maxpool_%s' % dtype), maxpool)

    return maxpool

# def fill_feed_dict(image_pl):
#     image_feed = ip.data_inputs('d:/tmp/img/img_data/input/', BATCH_SIZE)
#     feed_dict = {image_pl:image_feed}
#     return feed_dict

def train():    
    with tf.Graph().as_default() as g:
        examples = ip.data_inputs('d:/tmp/img/img_data/input/', BATCH_SIZE)
        logits = inference(examples, 'gaussblur')

        summary_op = tf.summary.merge_all()
        
        with tf.Session(graph=g) as sess:
            sess.run(tf.local_variables_initializer())
            sess.run(tf.global_variables_initializer())
            
            coord = tf.train.Coordinator()
            threads = tf.train.start_queue_runners(sess=sess, coord=coord)

            summary_writer = tf.summary.FileWriter('d:/tmp/img/img_train/', sess.graph)
            
            logits_op = sess.run(logits)
#             print(logits_op)

            summary_writer.add_summary(summary_op.eval())
            summary_writer.flush()

            coord.request_stop()
            coord.join(threads)

def main(argv=None):
    train()

if __name__ == '__main__':
    tf.app.run(main=main)
