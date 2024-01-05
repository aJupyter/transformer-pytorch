# step 4、 构建多头注意力层

import torch.nn as nn


# 现在接受的输入是将token embedding 和 position embedding相加的矩阵，维度为[batch_size, seq_len, dim_vector]

class MultiHeadAttention(nn.Module):
    # n_head即多头，其原理是将dim_vector分割为n_head个。
    def __init__(self, dim_vector, n_head):
        super().__init__()
        self.n_head = n_head

        # torch中的线性层就是对输入进行一个线性变换，其中会有一个 Weights 参数矩阵，是可学习的。
        # 也正是因为这个矩阵，让Linear层可以将输入的 in_features 变为 out_features。
        self.w_q = nn.Linear(dim_vector, dim_vector)
        self.w_k = nn.Linear(dim_vector, dim_vector)
        self.w_v = nn.Linear(dim_vector, dim_vector)

    def forward(self, q, k, v):
        # 1、这里的q k v输入在论文中其实都是一个输入即token embedding 和 position embedding相加的矩阵，通过linear层得到真正的q k v
        q, k, v = self.w_q(q), self.w_k(k), self.w_v(v)

        # 2、进行dim_vector的多头分割
        q, k, v = self.dim_head_split(q), self.dim_head_split(k), self.dim_head_split(v)

        # 3、进行注意力的计算

    def dim_head_split(self, tensor):
        """
        将q k v 在dim_vector维度上分割为指定的n_head个头

        :param tensor: [batch_size, seq_len, dim_vector]
        :return:  [batch_size, n_head, seq_len, dim_split]
        """
        batch_size, seq_len, dim_vector = tensor.size()
        dim_split = dim_vector // self.n_head

        # 这里view方法和transpose方法的联用有一些绕，需要弄清楚，transpose方法对a的后两维进行了转置交换，而view方法则是以行序对所有元素重新设定维度（见收藏的网页）。
        # 经过分割，我们的目标是得到上述return中的维度，若直接用view，虽然维度相同，但是运算中的数是都变了的。
        # 单维度来讲， 我们要的分割是把dim_vector长度 分割为 n_head 个 dim_split长度的
        tensor = tensor.view(batch_size, seq_len, self.n_head, dim_split)
        # 单维度分割好后，再进行转置以符合我们的数据组成格式
        tensor = tensor.transpose(1, 2)

        return tensor