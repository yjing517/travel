import pandas as pd
import numpy as np
import sys
sys.path.append("../..")
from tqdm import tqdm

from modelscope.models import Model
from modelscope.pipelines import pipeline
from modelscope.utils.constant import Tasks

model_id = "iic/nlp_gte_sentence-embedding_chinese-large"
pipeline_se = pipeline(Tasks.sentence_embedding,
                       model=model_id,
                       sequence_length=512 # 最大文本长度，默认值为128
                       )
# 当输入包含“soure_sentence”与“sentences_to_compare”时，会输出source_sentence中首个句子与sentences_to_compare中每个句子的向量表示，以及source_sentence中首个句子与sentences_to_compare中每个句子的相似度。
inputs = {
        "source_sentence": ["吃完海鲜可以喝牛奶吗?"],
        "sentences_to_compare": [
            "不可以，早晨喝牛奶不科学",
            "吃了海鲜后是不能再喝牛奶的，因为牛奶中含得有维生素C，如果海鲜喝牛奶一起服用会对人体造成一定的伤害",
            "吃海鲜是不能同时喝牛奶吃水果，这个至少间隔6小时以上才可以。",
            "吃海鲜是不可以吃柠檬的因为其中的维生素C会和海鲜中的矿物质形成砷"
        ]
    }

result = pipeline_se(input=inputs)
print (result)

# 当输入仅含有soure_sentence时，会输出source_sentence中每个句子的向量表示以及首个句子与其他句子的相似度。
inputs2 = {
        "source_sentence": [
            "可以，但是早上打篮球不科学",
            "可以，早晨喝牛奶不科学",
            "不可以，早晨打篮球不科学",
            "我喜欢打篮球",
            "早上可以打篮球吗"
        ]
}
result = pipeline_se(input=inputs2)
print (result)

v1 = result['text_embedding'][0]
v2 = result['text_embedding'][1]
v3 = result['text_embedding'][2]
v4 = result['text_embedding'][3]
v5 = result['text_embedding'][4]

def euclidean_distance(vector1, vector2):
  """
  计算两个向量之间的欧氏距离。
  """
  return np.linalg.norm(vector1 - vector2)

print(np.dot(v1, v2))
print(np.dot(v1, v3))
print(np.dot(v1, v4))
print(np.dot(v1, v5))

#
# if __name__ == '__main__':
#     aid_df = pd.read_csv(f"../List/aid_list.csv")

