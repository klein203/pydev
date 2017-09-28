'''
Created on 2017年9月18日

@author: xusheng
'''

import os
import tensorflow as tf
from PIL import Image

IMG_WIDTH_PIXEL = 1024
IMG_HEIGHT_PIXEL = 768
IMG_CHANNEL = 3

NUM_EXAMPLES_PER_EPOCH_FOR_TRAIN = 1

def _int64_feature(value):
    return tf.train.Feature(int64_list=tf.train.Int64List(value=[value]))

def _bytes_feature(value):
    return tf.train.Feature(bytes_list=tf.train.BytesList(value=[value]))

def img2tfrecord(data_path, target_file):
    filename_list = os.listdir(data_path)
    filename_list.sort()
#     labelname_list = [x.split('.')[0] for x in filename_list]
    num_examples = len(filename_list)

    with tf.python_io.TFRecordWriter(target_file) as fw:
        for i in range(num_examples):
            fullname = os.path.join(data_path, filename_list[i])
            image = Image.open(fullname, 'r')
            image_raw = image.tobytes()
#             print(len(image_raw))
            example = tf.train.Example(features=tf.train.Features(feature={
                'image_raw': _bytes_feature(image_raw),
                'label': _int64_feature(i),
                }))

            fw.write(example.SerializeToString())
    
def _generate_image_batch(image, min_queue_examples, batch_size):
    num_preprocess_threads = 1
#     images = tf.train.shuffle_batch([image], batch_size=batch_size, num_threads=num_preprocess_threads, capacity=min_queue_examples + 3 * batch_size, min_after_dequeue=min_queue_examples)
    images = tf.train.batch([image], batch_size=batch_size)
    tf.summary.image('images', images)
    return images

def read_image(filename_queue):
    reader = tf.TFRecordReader()
    _, images = reader.read(filename_queue)
    
    features = tf.parse_single_example(images, features={
          'image_raw': tf.FixedLenFeature([], tf.string),
          })
    image = tf.decode_raw(features['image_raw'], tf.uint8)
    image = tf.reshape(image, [IMG_HEIGHT_PIXEL, IMG_WIDTH_PIXEL, IMG_CHANNEL])
    return image

def data_inputs(data_dir, batch_size):
    filename_list = os.listdir(data_dir)
    filename_list = [os.path.join(data_dir, x) for x in filename_list]
    filename_queue = tf.train.string_input_producer(filename_list, num_epochs=1, shuffle=False)
    image = read_image(filename_queue)
    float_image = tf.cast(image, tf.float32)
    float_image = float_image / 256.
    
    min_fraction_of_examples_in_queue = 0.4
    min_queue_examples = int(NUM_EXAMPLES_PER_EPOCH_FOR_TRAIN * min_fraction_of_examples_in_queue) # int(1*0.4) = 0
#     print ('Filling queue with %d images before starting to train. This will take a few minutes.' % min_queue_examples)
    return _generate_image_batch(float_image, min_queue_examples, batch_size)

if __name__ == '__main__':
    with tf.Graph().as_default() as g:
        examples = data_inputs('d:/tmp/img/img_data/input/', 1)
        with tf.Session(graph=g) as sess:
            sess.run(tf.local_variables_initializer())
            sess.run(tf.global_variables_initializer())
            
            coord = tf.train.Coordinator()
            threads = tf.train.start_queue_runners(sess=sess, coord=coord)
                
            op = sess.run(examples)
            print('op =', op)
    
            coord.request_stop()
            coord.join(threads)
