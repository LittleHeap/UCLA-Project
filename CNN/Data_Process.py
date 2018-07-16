import random
from functools import reduce
import matplotlib.pyplot as plt
import time
from scipy.io import *
import spectral
from spectral import *
import joblib
from sklearn.model_selection import *
import numpy as np
from sklearn.svm import SVC
from sklearn import *
import pandas as pd
import tensorflow as tf

'''
    1.获取9个类别，每个类别200条，一共1800条数据，每条数据103通道信息+一列label，一共(1800,104)
'''
'''
# 导入数据集切割训练与测试数据（用最后处理出的最标准的数据，标准化统一）
data = pd.read_csv('../dataset/PaviaU_gt_band_label_loc_.csv', header=None)
data = data.as_matrix()

# 获取特征矩阵
data_content = data[:, :-2]
# print(data_content.shape)  # (42776, 103)

# 获取标记矩阵
data_label = data[:, -2]
# print(data_label.shape)  # (42776,)

# 切割训练集测试集
data_train, data_test, label_train, label_test = train_test_split(data_content, data_label, test_size=0.3)

# print(data_train.shape)  # (29943, 103)
# print(data_test.shape)  # (12833, 103)
# print(label_train.shape)  # (29943,)
# print(label_test.shape)  # (12833,)

# 获取不同类别指定个数的通道数据，返回该类别二维通道数据，类别label和行数number指定，通道数为103，104通道为label
def get_band(label, n):
    band = []
    for i in range(42776):
        currentband = list(data_content[i])
        currentlabel = data_label[i]
        currentband.append(label)
        if currentlabel == label:
            band.append(currentband)
        if len(list(band)) == n:
            break
    band = list(band)
    # print(len(band))
    band_matrix = np.array(band)
    # print(band.shape)
    # print(band_matrix)
    return band_matrix


data = list()

for i in range(10):
    if i == 0:
        continue
    band_i = get_band(i, 200)
    for j in range(200):
        row = band_i[j, :]
        data.append(row)

new_data = pd.DataFrame(data)
print(new_data.shape)
new_data.to_csv('./dataset/CNN_data.csv', header=False, index=False)
'''

'''
    2.将1800条数据打乱顺序
'''
'''
# 导入数据集切割训练与测试数据（用最后处理出的最标准的数据，标准化统一）
data = pd.read_csv('./dataset/CNN_data.csv', header=None)
data = data.as_matrix()

# 获取特征矩阵
data_content = data[:, :-1]
print(data_content.shape)  # (1800, 103)

# 获取标记矩阵
data_label = data[:, -1]
print(data_label.shape)  # (1800,)

new_csv = []

for i in range(1800):
    new_csv.append(data[i])

random.shuffle(new_csv)
new_csv = pd.DataFrame(new_csv)
new_csv.to_csv('./dataset/CNN_data_shuffle.csv', header=False, index=False)
'''

'''
    3.将标签转化为onehot矩阵格式，并存储
'''
'''
# onehot函数
def onehot(labels, length):
    sess = tf.Session()
    batch_size = tf.size(labels)  # 5
    labels = tf.expand_dims(labels, 1)
    indices = tf.expand_dims(tf.range(0, batch_size, 1), 1)
    concated = tf.concat([indices, labels], 1)
    onehot_labels = tf.sparse_to_dense(concated, tf.stack([batch_size, length]), 1.0, 0.0)
    # print(sess.run(onehot_labels))
    return onehot_labels


# onehot([1, 3, 5, 7, 9], 10)



# 导入乱序数据集切割训练与测试数据（用最后处理出的最标准的数据，标准化统一）
data = pd.read_csv('./dataset/CNN_data_shuffle.csv', header=None)
data = data.as_matrix()

# 获取特征矩阵
data_content = data[:, :-1]
print(data_content.shape)  # (1800, 103)

# 获取标记矩阵
data_label = data[:, -1]
print(data_label.shape)  # (1800,)

label = []

for i in range(1800):
    label.append(int(data_label[i]))

onehot_label = onehot(label, 10)

print(onehot_label)
print(onehot_label.shape)  # (1800, 10)

onehot_csv = []

sess = tf.Session()

for i in range(1800):
    onehot_csv.append(sess.run(onehot_label[i]))

onehot_csv = pd.DataFrame(onehot_csv)
onehot_csv.to_csv('./dataset/CNN_data_shuffle_onehot_label.csv', header=False, index=False)
'''

'''
    4.分别按批次读取通道数据和onehot标记数据过程操作
'''
data_band = pd.read_csv('./dataset/CNN_data_shuffle.csv', header=None)
data_band = data_band.as_matrix()

# 获取特征矩阵
data_band = data_band[:, :-1]
print(data_band.shape)  # (1800, 103)
