'''
Created on 2017年9月19日

@author: xusheng
'''
import numpy as np
import tensorflow as tf
# import matplotlib.pyplot as plt

IMG_WIDTH_PIXEL = 1024
IMG_HEIGHT_PIXEL = 768
IMG_CHANNEL = 3

def inputs(path):
    """Construct input for image inversion using the Reader ops.
    Args:
        path: Full path of image file.
    Returns:
        image: Image. 4D tensor of [IMG_WIDTH_PIXEL, IMG_HEIGHT_PIXEL, IMG_CHANNEL] size.
    """
    reader = tf.WholeFileReader()
    _, value = reader.read(tf.train.string_input_producer([path]))
    image = tf.image.decode_jpeg(value)
#     image = tf.image.convert_image_dtype(image, tf.float32)
    image = tf.reshape(image, [1, IMG_WIDTH_PIXEL, IMG_HEIGHT_PIXEL, IMG_CHANNEL])
    image = tf.get_variable('x', initializer=tf.to_float(image))

    return image

def inference(image, dtype='sharpen'):
    """Build the image inversion model.
    Args:
        image: Image returned from inputs().
        dtype: Different types of image inversion. eg: sharpen
    Returns:
        logits.
    """

    if dtype == 'sharpen':
        k = np.ones([3, 3, 3, 3]) * -1
        k[1, 1, :, :] = 9
    else: # default sharpen
        k = np.ones([3, 3, 3, 3]) * -1
        k[1, 1, :, :] = 9

    w = tf.get_variable('w', initializer=tf.to_float(k))
#     w = tf.constant(k, dtype=tf.float32, shape=[3, 3, 3, 3])

    conv = tf.nn.conv2d(image, w, [1, 3, 3, 1], 'SAME')
#     tf.summary.image('conv_op', conv)
    
    sigmoid = tf.sigmoid(conv)
#     tf.summary.image('sigmoid_op', sigmoid)

    maxpool = tf.nn.max_pool(sigmoid, [1, 3, 3, 1], [1, 3, 3, 1], 'SAME')
#     tf.summary.image('maxpool_op', maxpool)

    return maxpool

if __name__ == '__main__':
    with tf.Graph().as_default():
        image = inputs('d:/tmp/img/Hydrangeas.jpg')
        logits = inference(image, 'sharpen')
#         summary_op = tf.summary.merge_all()
        
        init = tf.global_variables_initializer()
        with tf.Session() as sess:
            sess.run(init)
            # get stuck here
            logits_op = sess.run(logits)

#             summary_writer = tf.summary.FileWriter('d:/tmp/img/', sess.graph)
#             summary_str = sess.run(summary_op)
#             summary_writer.add_summary(summary_str)
#             summary_writer.flush()