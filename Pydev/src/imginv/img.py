'''
Created on 2017年9月19日

@author: xusheng
'''
import numpy as np
import tensorflow as tf
import imginv.img_input as ip

BATCH_SIZE = 3

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
    tf.summary.image(('%s_1_conv_op' % dtype), conv)
    
#     sigmoid = tf.sigmoid(conv, name='sig')
#     tf.summary.image(('%s_2_sig_op' % dtype), sigmoid)
 
    maxpool = tf.nn.max_pool(conv, [1, 3, 3, 1], [1, 3, 3, 1], 'SAME', name='pool')
    tf.summary.image(('%s_3_maxpool_op' % dtype), maxpool)

    return maxpool

# def fill_feed_dict(image_pl):
#     image_feed = ip.data_inputs('d:/tmp/img/img_data/input/', BATCH_SIZE)
#     feed_dict = {image_pl:image_feed}
#     return feed_dict

def train():    
    with tf.Graph().as_default() as g:
        examples = ip.data_inputs('d:/tmp/img/img_data/input/', BATCH_SIZE)
        origin_logits = inference(examples, 'origin')
        sharpen_logits = inference(examples, 'sharpen')
        edge_logits = inference(examples, 'edge')
        boxblur_logits = inference(examples, 'boxblur')
        gaussblur_logits = inference(examples, 'gaussblur')

        summary_op = tf.summary.merge_all()
        
        with tf.Session(graph=g) as sess:
            sess.run(tf.local_variables_initializer())
            sess.run(tf.global_variables_initializer())
            
            coord = tf.train.Coordinator()
            threads = tf.train.start_queue_runners(sess=sess, coord=coord)

            summary_writer = tf.summary.FileWriter('d:/tmp/img/img_train/', sess.graph)
            
            origin_logits_op, sharpen_logits_op, edge_logits_op, boxblur_logits_op, gaussblur_logits_op = sess.run([origin_logits, sharpen_logits, edge_logits, boxblur_logits, gaussblur_logits])
#             print(logits_op)

            summary_writer.add_summary(summary_op.eval())
            summary_writer.flush()

            coord.request_stop()
            coord.join(threads)

def main(argv=None):
    train()

if __name__ == '__main__':
    '''
        CMD: tensorboard --logdir=D://tmp//img//img_train
    '''
    tf.app.run(main=main)
