'''
Created on 2017年10月6日

@author: xusheng
'''

import tensorflow as tf
import math
from sklearn import datasets
from sklearn.manifold import TSNE
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import cm
# from mpl_toolkits.mplot3d import Axes3D
import seaborn as sns

class TF_PCA:
    def __init__(self, data, target=None, dtype=tf.float32):
        self.data = data
        self.target = target
        self.dtype = dtype

        self.graph = None
        self.X = None
        self.u = None
        self.v = None
        self.singular_values = None
        self.sigma = None

    def fit(self):
        self.graph = tf.Graph()
        with self.graph.as_default():
            self.X = tf.placeholder(self.dtype, shape=self.data.shape)

            # Perform SVD
            singular_values, u, v = tf.svd(self.X, full_matrices=True)

            # Create sigma matrix
            sigma_np = np.zeros((self.data.shape[0], self.data.shape[1]), dtype=np.float32)
            for i in range(self.data.shape[1]):
                sigma_np[i, i] = 1
            
            sigma = tf.matmul(tf.constant(sigma_np, dtype=tf.float32), tf.diag(singular_values))

        with tf.Session(graph=self.graph) as session:
            self.u, self.singular_values, self.sigma, self.v = session.run([u, singular_values, sigma, v], feed_dict={self.X: self.data})

    def reduce(self, n_dimensions=None, keep_info=None):
        if keep_info:
            # Normalize singular values
            normalized_singular_values = self.singular_values / sum(self.singular_values)
#             print("normalized_singular_values", normalized_singular_values)
            
            # Create the aggregated ladder of kept information per dimension
            ladder = np.cumsum(normalized_singular_values)
#             print("ladder", ladder, ladder.shape)

            # Get the first index which is above the given information threshold
            index = next(idx for idx, value in enumerate(ladder) if value >= keep_info) + 1
            n_dimensions = index
            print("Reduce dimensionality from %d to %d" % (self.data.shape[1], n_dimensions))
            
        with self.graph.as_default():
            # Cut out the relevant part from u, N x P
            u = tf.slice(self.u, [0, 0], [self.data.shape[0], n_dimensions])
            # Cut out the relevant part from sigma, P x P
            sigma = tf.slice(self.sigma, [0, 0], [n_dimensions, n_dimensions])            
            # Cut out the relevant part from vt, P x M
            v = tf.slice(self.v, [0, 0], [self.data.shape[1], n_dimensions])

            # PCA, N x P x M
            pca = tf.matmul(tf.matmul(u, sigma), tf.transpose(v))
            
            ori_pca = tf.matmul(tf.matmul(self.u, self.sigma), tf.transpose(self.v))

        with tf.Session(graph=self.graph) as session:
            return session.run([u, sigma, v, pca, ori_pca], feed_dict={self.X: self.data})

def createDataSet(filename):
    dataSet = []
    with open(filename, 'r', encoding='utf-8') as fr:
        for line in fr.readlines():
            record = [int(x) for x in line.strip().split(',')]
            dataSet.append(record)
    return dataSet

if __name__ == '__main__':
    dataset = createDataSet("d:/tmp/abc.csv")
    ar = np.array(dataset)

#     ar = np.random.rand(100, 20)
    print(ar)
    
    tf_pca = TF_PCA(ar)
    tf_pca.fit()
#     print("u", tf_pca.u, tf_pca.u.shape)
#     print("singular_values", tf_pca.singular_values, tf_pca.singular_values.shape)
#     print("sigma", tf_pca.sigma, tf_pca.sigma.shape)
#       
    u, sigma, vt, pca, ori_pca = tf_pca.reduce(keep_info=0.98)  # Results in two dimensions
#     print("pca", pca, pca.shape, type(pca))

    resultfilename = "d:/tmp/orgin.csv"
    with open(resultfilename, 'w', encoding='utf-8') as fw:
        for row in ori_pca.tolist():
            line = ', '.join([str(x) for x in row])
            line = line + '\n'
#             print(line)
            fw.write(line)
            
    resultfilename = "d:/tmp/result.csv"
    with open(resultfilename, 'w', encoding='utf-8') as fw:
        for row in pca.tolist():
            line = ', '.join([str(x) for x in row])
            line = line + '\n'
#             print(line)
            fw.write(line)
     
#     color_mapping = {0: sns.xkcd_rgb['bright purple'], 1: sns.xkcd_rgb['lime'], 2: sns.xkcd_rgb['ochre']}
#     colors = list(map(lambda x: color_mapping[x], iris_dataset.target))
#      
#     plt.scatter(pca[:, 0], pca[:, 1], c=colors)
#     plt.show()

# def demo():
#     iris_dataset = datasets.load_iris()
# #     print(type(iris_dataset.data))
#      
#     tf_pca = TF_PCA(iris_dataset.data, iris_dataset.target)
#     tf_pca.fit()
#      
#     pca = tf_pca.reduce(keep_info=0.9)  # Results in two dimensions
#      
#     color_mapping = {0: sns.xkcd_rgb['bright purple'], 1: sns.xkcd_rgb['lime'], 2: sns.xkcd_rgb['ochre']}
#     colors = list(map(lambda x: color_mapping[x], iris_dataset.target))
#      
#     plt.scatter(pca[:, 0], pca[:, 1], c=colors)
#     plt.show()
