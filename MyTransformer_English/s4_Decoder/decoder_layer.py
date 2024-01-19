# step 4.1、encoder layer
import torch.nn as nn
from MyTransformer_English.s2_MultiHeadAttention.muti_head_attention import MultiHeadAttention
from MyTransformer_English.s2_MultiHeadAttention.feed_forward import FeedForward


class DecoderLayer(nn.Module):
    """
        Decoder Layer

        Args:
            dim_vector: the dimension of embedding vector for each input word.
            n_head: Number of heads
            dim_hidden: The parameter in the feedforward layer
            dropout: probability of an element to be zeroed.
    """
    def __init__(self, dim_vector, n_head, dropout, dim_hidden):
        super().__init__()
        # 1、The first attention layer and add&norm in decoder
        self.attention_1 = MultiHeadAttention(dim_vector, n_head)
        self.norm1 = nn.LayerNorm(dim_vector)
        self.dropout1 = nn.Dropout(dropout)

        # 2、 The second attention layer and add&norm in decoder
        self.attention_2 = MultiHeadAttention(dim_vector, n_head)
        self.norm2 = nn.LayerNorm(dim_vector)
        self.dropout2 = nn.Dropout(dropout)

        # 3、Feedforward and add&norm
        self.feedforward = FeedForward(dim_vector, dim_hidden, dropout)
        self.norm2 = nn.LayerNorm(dim_vector)
        self.dropout3 = nn.Dropout(dropout)

    def forward(self, encoder_output, decoder_input, trg_mask, src_mask):
        # 1、与编码层一样，第一步是计算注意力
        # 这里的trg_mask是用于使decoder中前面词无法使用到后面词的信息，并且也需要考虑padding。
        _input = decoder_input
        x = self.attention_1(q=decoder_input, k=decoder_input, v=decoder_input, mask=trg_mask)

        # 2、 Add&Norm
        x = self.dropout1(x)
        x = self.norm1(x + _input)

        # 3、 第二层注意力计算
        # 这里的src_mask是用于encoder中当句子长度不一时，需要将所有的句子填充至相同的长度。
        _input = x
        x = self.attention_2(q=x, k=encoder_output, v=encoder_output, mask=src_mask)

        # 4、 Add&Norm
        x = self.dropout2(x)
        x = self.norm1(x + _input)

        # 5、feedforward
        _input = x
        x = self.feedforward(x)

        # 6、 Add&Norm
        x = self.dropout3(x)
        x = self.norm1(x + _input)

        return x
