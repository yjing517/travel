import pandas as pd
import numpy as np
import os
import sys
import csv
sys.path.append("../..")
from tqdm import tqdm
import ast
import xml.etree.ElementTree as ET
# 设置 pandas 显示所有列和行
pd.set_option('display.max_columns', None)  # 显示所有列
pd.set_option('display.max_rows', None)     # 显示所有行
pd.set_option('display.width', None)        # 自动调整列宽
pd.set_option('display.max_colwidth', None) # 显示所有字符
from transformers import AutoModelForSequenceClassification

model = AutoModelForSequenceClassification.from_pretrained(
    'C:/Users/Yuanx/.cache/huggingface/hub/models--jinaai--jina-reranker-v2-base-multilingual/snapshots/6371035883584acb0584c34dbaa9350e4752b8d2',
    torch_dtype="auto",
    trust_remote_code=True,
    use_flash_attn=False,
)
model.to('cuda')
model.eval()


# 解析 XML 字符串
def parse_xml(xml_string):
    root = ET.fromstring(xml_string)
    result = {}
    for child in root:
        if child.tag == 'd':
            # 解析 <d> 标签中的属性
            attributes = child.attrib['p'].split(',')
            content = child.text
            result[child.tag + '_' + str(len(result))] = {
                'attributes': attributes,
                'content': content
            }
        else:
            result[child.tag] = child.text
    return result

# 提取 d 标签中的 content 并存储在列表中
def extract_d_content(parsed_data):
    d_content_list = []
    for key, value in parsed_data.items():
        if key.startswith('d_'):
            d_content_list.append(value['content'])
    return d_content_list

def cal_content_similarity(aid_df,reply_df,similarity_df):
    print(aid_df.shape)
    print(reply_df.shape)
    print(f'开始计算语义相关性：title-text')

    pbar = tqdm(total=len(aid_df))
    
    # reply_df['reply'] = reply_df['reply'].apply(ast.literal_eval)
    reply_df['danmaku'] = reply_df['danmaku'].apply(parse_xml)
    reply_df['danmaku'] = reply_df['danmaku'].apply(extract_d_content)

    for index, row in aid_df.iterrows():
        aid = int(row['aid'])
        # 已完成计算
        if aid in similarity_df['aid'].values:
            pass
        # 未完成计算
        else:
            query = row['title']
            
            # reply_list = reply_df[reply_df['aid']==aid]['reply'].apply(lambda x: x.get('message')).tolist()
            reply_list = reply_df[reply_df['aid']==aid]['danmaku'].tolist()
            if reply_list:
                reply_list = reply_list[0]

            if reply_list:
                sentence_pairs = [[query, reply] for reply in reply_list]
                scores = model.predict(sentence_pairs, max_length=1024)
                # with open(f"./Result/title_reply_similarity.csv", 'a+', newline='',encoding='utf-8') as file:
                with open(f"./Result/title_danmaku_similarity.csv", 'a+', newline='',encoding='utf-8') as file:
                    writer = csv.writer(file)
                    writer.writerows([[aid,query,scores]])
        pbar.update(1)
    pbar.close()

    print('完成计算语义相关性：title-text')

if __name__ == '__main__':

    aid_df = pd.read_csv(f"./List/aid_list.csv",encoding='utf-8')

    # 评论
    # if os.path.exists(f"./Result/title_reply_similarity.csv"):
    #     similarity_df = pd.read_csv(f"./Result/title_reply_similarity.csv",encoding='utf-8')
    # else:
    #     similarity_df = pd.DataFrame(columns=['aid','title','title_reply_similarity'])
    #     similarity_df.to_csv(f"./Result/title_reply_similarity.csv", index=False,encoding='utf-8')
    # reply_df = pd.read_csv(f"./List/reply.csv",encoding='utf-8')
    # cal_content_similarity(aid_df,reply_df,similarity_df)

    # 弹幕
    # if os.path.exists(f"./Result/title_danmaku_similarity.csv"):
    #     similarity_df = pd.read_csv(f"./Result/title_danmaku_similarity.csv",encoding='utf-8')
    # else:
    #     similarity_df = pd.DataFrame(columns=['aid','title','title_danmaku_similarity'])
    #     similarity_df.to_csv(f"./Result/title_danmaku_similarity.csv", index=False,encoding='utf-8')
    # danmaku_df = pd.read_csv(f"./List/danmaku.csv",encoding='utf-8')
    # cal_content_similarity(aid_df,danmaku_df,similarity_df)


