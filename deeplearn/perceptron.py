#!/user/bin/env python
# encoding: utf-8
#@time      : 2019/9/26 16:31
from functools import reduce

__author__ = 'Ethan'


class Perceptron(object):
    def __init__(self, input_num, activator):
        """
        激活感知器，设置输入参数的个数，以及激活函数
        激活函数的类型为double -> double
        :param input_num:
        :param activator:
        """
        self.activator = activator
        # 权重向量初始化为0
        self.weights = [0.0 for _ in range(input_num)]
        # 偏置初始化为0
        self.bias = 0.0

    def __str__(self):
        """
        print the learning weights and bias
        :return:
        """
        return 'weights\t:%s\nbias\t:%f\n' % (self.weights, self.bias)

    def predict(self, input_vec):
        """
        output vector, preception result
        :param input_vec:
        :return:
        """
        # 把input_vec[x1,x2,x3...]和wights[w1,w2,w3...]打包在一起
        # 变成[(x1,w1),(x2,w2),(x3,w3)...]
        # 然后利用map函数计算[x1*w1,x2*w2,x3*w3]
        # 最后利用reduce求和
        return self.activator(
            reduce(lambda a, b: a + b,
                   map(lambda x_w: x_w[0] * x_w[1],
                       zip(input_vec, self.weights))
                   , 0.0) + self.bias)

    def train(self, input_vecs, labels, interation, rate):
        """
        输入训练数据：一组向量，与每个向量对应的lable;以及训练轮数、学习率
        :param input_vec:
        :param lables:
        :param interation:
        :param rate:
        :return:
        """
        for i in range(interation):
            self._one_interation(input_vecs, labels, rate)

    def _one_interation(self, input_vecs, labels, rate):
        """
        一次迭代，把所有的训练数据过一遍
        :param input_vecs:
        :param lables:
        :param rate:
        :return:
        """
        # 把输入和输出打包在一起，成为样本的列表[(input_vec,label),...]
        # 而每个训练样本是(input_vec, label)
        samples = zip(input_vecs, labels)
        # 对每个样本，按照感知器的规则更新权重
        for (input_vec, label) in samples:
            # 计算感知器在当前权重下的输出
            output = self.predict(input_vec)
            # update weight
            self._update_weights(input_vec, output, label, rate)

