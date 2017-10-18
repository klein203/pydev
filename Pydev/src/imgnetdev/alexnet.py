'''
Created on 2017年10月18日

@author: xusheng
'''

import argparse
import os
import re
import sys
import tarfile

from six.moves import urllib
import tensorflow as tf

from imgnetdev import imgnet_input

parser = argparse.ArgumentParser()

# Basic model parameters.
parser.add_argument('--batch_size', type=int, default=128, help='Number of images to process in a batch.')
parser.add_argument('--data_dir', type=str, default='D:/tmp/imagenet/imagenet_data', help='Path to the data directory.')

FLAGS = parser.parse_args()

IMAGE_SIZE = imgnet_input.IMAGE_SIZE
NUM_CLASSES = imgnet_input.NUM_CLASSES
NUM_EXAMPLES_PER_EPOCH_FOR_TRAIN = imgnet_input.NUM_EXAMPLES_PER_EPOCH_FOR_TRAIN
NUM_EXAMPLES_PER_EPOCH_FOR_EVAL = imgnet_input.NUM_EXAMPLES_PER_EPOCH_FOR_EVAL


MOVING_AVERAGE_DECAY = 0.9999  # The decay to use for the moving average.
NUM_EPOCHS_PER_DECAY = 350.0  # Epochs after which learning rate decays.
LEARNING_RATE_DECAY_FACTOR = 0.1  # Learning rate decay factor.
INITIAL_LEARNING_RATE = 0.1  # Initial learning rate.

TOWER_NAME = 'tower'

DATA_URL = 'http://www.cs.toronto.edu/~kriz/cifar-10-binary.tar.gz'


def _activation_summary(x):
    # Remove 'tower_[0-9]/' from the name in case this is a multi-GPU training
    # session. This helps the clarity of presentation on tensorboard.
    tensor_name = re.sub('%s_[0-9]*/' % TOWER_NAME, '', x.op.name)
    tf.summary.histogram(tensor_name + '/activations', x)
    tf.summary.scalar(tensor_name + '/sparsity', tf.nn.zero_fraction(x))

def _variable_on_cpu(name, shape, initializer):
    with tf.device('/cpu:0'):
        var = tf.get_variable(name, shape, initializer=initializer, dtype=tf.float32)
    return var

def _variable_with_weight_decay(name, shape, stddev, wd):
    var = _variable_on_cpu(name, shape, tf.truncated_normal_initializer(stddev=stddev, dtype=tf.float32))
    if wd is not None:
        weight_decay = tf.multiply(tf.nn.l2_loss(var), wd, name='weight_loss')
        tf.add_to_collection('losses', weight_decay)
    return var

def distorted_inputs():
    if not FLAGS.data_dir:
        raise ValueError('Please supply a data_dir')
    data_dir = os.path.join(FLAGS.data_dir, 'cifar-10-batches-bin')
    images, labels = imgnet_input.distorted_inputs(data_dir=data_dir, batch_size=FLAGS.batch_size)

    return images, labels

def inputs(eval_data):
    if not FLAGS.data_dir:
        raise ValueError('Please supply a data_dir')
    data_dir = os.path.join(FLAGS.data_dir, 'cifar-10-batches-bin')
    images, labels = imgnet_input.inputs(eval_data=eval_data, data_dir=data_dir, batch_size=FLAGS.batch_size)
    
    return images, labels

def inference(images):
    # conv1
    with tf.variable_scope('conv1') as scope:
        kernel = _variable_with_weight_decay('weights', shape=[11, 11, 3, 96], stddev=1e-1, wd=0.0)
        conv = tf.nn.conv2d(images, kernel, [1, 4, 4, 1], padding='SAME')
        biases = _variable_on_cpu('biases', [96], tf.constant_initializer(0.1))
        pre_activation = tf.nn.bias_add(conv, biases)
        conv1 = tf.nn.relu(pre_activation, name=scope.name)
        _activation_summary(conv1)

    # pool1
    with tf.variable_scope('pool1') as scope:
        pool1 = tf.nn.max_pool(conv1, ksize=[1, 3, 3, 1], strides=[1, 2, 2, 1], padding='VALID')

    # lrn1
    with tf.variable_scope('lrn1') as scope:
        norm1 = tf.nn.lrn(pool1, depth_radius=5, bias=2.0, alpha=1e-4, beta=0.75)

    # conv2
    with tf.variable_scope('conv2') as scope:
        kernel = _variable_with_weight_decay('weights', shape=[5, 5, 96, 256], stddev=1e-1, wd=0.0)
        conv = tf.nn.conv2d(norm1, kernel, [1, 1, 1, 1], padding='SAME')
        biases = _variable_on_cpu('biases', [256], tf.constant_initializer(0.1))
        pre_activation = tf.nn.bias_add(conv, biases)
        conv2 = tf.nn.relu(pre_activation, name=scope.name)
        _activation_summary(conv2)

    # pool2
    with tf.variable_scope('pool2') as scope:
        pool2 = tf.nn.max_pool(conv2, ksize=[1, 3, 3, 1], strides=[1, 2, 2, 1], padding='VALID')

    # lrn2
    with tf.variable_scope('lrn2') as scope:
        norm2 = tf.nn.lrn(pool2, 5, bias=2.0, alpha=1e-4, beta=0.75)

    # conv3
    with tf.variable_scope('conv3') as scope:
        kernel = _variable_with_weight_decay('weights', shape=[3, 3, 256, 384], stddev=1e-1, wd=0.0)
        conv = tf.nn.conv2d(norm2, kernel, [1, 1, 1, 1], padding='SAME')
        biases = _variable_on_cpu('biases', [384], tf.constant_initializer(0.1))
        pre_activation = tf.nn.bias_add(conv, biases)
        conv3 = tf.nn.relu(pre_activation, name=scope.name)
        _activation_summary(conv3)

    # conv4
    with tf.variable_scope('conv4') as scope:
        kernel = _variable_with_weight_decay('weights', shape=[3, 3, 384, 384], stddev=1e-1, wd=0.0)
        conv = tf.nn.conv2d(conv3, kernel, [1, 1, 1, 1], padding='SAME')
        biases = _variable_on_cpu('biases', [384], tf.constant_initializer(0.1))
        pre_activation = tf.nn.bias_add(conv, biases)
        conv4 = tf.nn.relu(pre_activation, name=scope.name)
        _activation_summary(conv4)

    # conv5
    with tf.variable_scope('conv5') as scope:
        kernel = _variable_with_weight_decay('weights', shape=[3, 3, 384, 256], stddev=1e-1, wd=0.0)
        conv = tf.nn.conv2d(conv3, kernel, [1, 1, 1, 1], padding='SAME')
        biases = _variable_on_cpu('biases', [256], tf.constant_initializer(0.1))
        pre_activation = tf.nn.bias_add(conv, biases)
        conv5 = tf.nn.relu(pre_activation, name=scope.name)
        _activation_summary(conv5)
          
    # pool5
    with tf.variable_scope('pool5') as scope:
        pool5 = tf.nn.max_pool(conv5, ksize=[1, 3, 3, 1], strides=[1, 2, 2, 1], padding='VALID')
                          
    # fc6
    with tf.variable_scope('fc6') as scope:
        reshape = tf.reshape(pool5, [FLAGS.batch_size, -1])
        dim = reshape.get_shape()[1].value
        weights = _variable_with_weight_decay('weights', shape=[dim, 4096], stddev=0.04, wd=0.0)
        biases = _variable_on_cpu('biases', [4096], tf.constant_initializer(0.1))
        fc6 = tf.nn.relu(tf.matmul(reshape, weights) + biases, name=scope.name)
        _activation_summary(fc6)

    # fc7
    with tf.variable_scope('fc7') as scope:
        weights = _variable_with_weight_decay('weights', shape=[4096, 4096], stddev=0.04, wd=0.0)
        biases = _variable_on_cpu('biases', [4096], tf.constant_initializer(0.1))
        fc7 = tf.nn.relu(tf.matmul(fc6, weights) + biases, name=scope.name)
        _activation_summary(fc7)
    
    # fc8
    with tf.variable_scope('fc8') as scope:
        weights = _variable_with_weight_decay('weights', shape=[4096, 1000], stddev=0.04, wd=0.0)
        biases = _variable_on_cpu('biases', [1000], tf.constant_initializer(0.1))
        fc8 = tf.nn.relu(tf.matmul(fc7, weights) + biases, name=scope.name)
        _activation_summary(fc8)

    # output
    with tf.variable_scope('softmax') as scope:
        weights = _variable_with_weight_decay('weights', [1000, NUM_CLASSES], stddev=1e-4, wd=0.0)
        biases = _variable_on_cpu('biases', [NUM_CLASSES], tf.constant_initializer(0.0))
        softmax = tf.add(tf.matmul(fc8, weights), biases, name=scope.name)
        _activation_summary(softmax)

    return softmax

def loss(logits, labels):
    labels = tf.cast(labels, tf.int64)
    cross_entropy = tf.nn.sparse_softmax_cross_entropy_with_logits(labels=labels, logits=logits, name='cross_entropy_per_example')
    cross_entropy_mean = tf.reduce_mean(cross_entropy, name='cross_entropy')
    tf.add_to_collection('losses', cross_entropy_mean)

    return tf.add_n(tf.get_collection('losses'), name='total_loss')

def _add_loss_summaries(total_loss):
    loss_averages = tf.train.ExponentialMovingAverage(0.9, name='avg')
    losses = tf.get_collection('losses')
    loss_averages_op = loss_averages.apply(losses + [total_loss])

    for l in losses + [total_loss]:
        tf.summary.scalar(l.op.name + ' (raw)', l)
        tf.summary.scalar(l.op.name, loss_averages.average(l))

    return loss_averages_op

def train(total_loss, global_step):
    num_batches_per_epoch = NUM_EXAMPLES_PER_EPOCH_FOR_TRAIN / FLAGS.batch_size
    decay_steps = int(num_batches_per_epoch * NUM_EPOCHS_PER_DECAY)

    lr = tf.train.exponential_decay(INITIAL_LEARNING_RATE, global_step, decay_steps, LEARNING_RATE_DECAY_FACTOR, staircase=True)
    tf.summary.scalar('learning_rate', lr)

    loss_averages_op = _add_loss_summaries(total_loss)

    with tf.control_dependencies([loss_averages_op]):
        opt = tf.train.GradientDescentOptimizer(lr)
        grads = opt.compute_gradients(total_loss)

    apply_gradient_op = opt.apply_gradients(grads, global_step=global_step)

    for var in tf.trainable_variables():
        tf.summary.histogram(var.op.name, var)

    for grad, var in grads:
        if grad is not None:
            tf.summary.histogram(var.op.name + '/gradients', grad)

    # Track the moving averages of all trainable variables.
    variable_averages = tf.train.ExponentialMovingAverage(MOVING_AVERAGE_DECAY, global_step)
    variables_averages_op = variable_averages.apply(tf.trainable_variables())

    with tf.control_dependencies([apply_gradient_op, variables_averages_op]):
        train_op = tf.no_op(name='train')

    return train_op


def maybe_download_and_extract():
    """Download and extract the tarball from Alex's website."""
    dest_directory = FLAGS.data_dir
    if not os.path.exists(dest_directory):
        os.makedirs(dest_directory)
    filename = DATA_URL.split('/')[-1]
    filepath = os.path.join(dest_directory, filename)
    if not os.path.exists(filepath):
        def _progress(count, block_size, total_size):
            sys.stdout.write('\r>> Downloading %s %.1f%%' % (filename, float(count * block_size) / float(total_size) * 100.0))
            sys.stdout.flush()
        filepath, _ = urllib.request.urlretrieve(DATA_URL, filepath, _progress)
        print()
        statinfo = os.stat(filepath)
        print('Successfully downloaded', filename, statinfo.st_size, 'bytes.')
    extracted_dir_path = os.path.join(dest_directory, 'cifar-10-batches-bin')
    if not os.path.exists(extracted_dir_path):
        tarfile.open(filepath, 'r:gz').extractall(dest_directory)

if __name__ == '__main__':
    images = tf.random_normal([1, 227, 227, 3], mean=0.1, stddev=0.1, dtype=tf.float32)
    inference = inference(images)
    
    init = tf.global_variables_initializer()
    with tf.Session() as sess:
        sess.run(init)
        print(inference.eval())
    