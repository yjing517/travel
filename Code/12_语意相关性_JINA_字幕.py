import pandas as pd
import numpy as np
import os
import sys
import csv
sys.path.append("../..")
from tqdm import tqdm
from transformers import AutoModelForSequenceClassification

model = AutoModelForSequenceClassification.from_pretrained(
    'C:/Users/Yuanx/.cache/huggingface/hub/models--jinaai--jina-reranker-v2-base-multilingual/snapshots/6371035883584acb0584c34dbaa9350e4752b8d2',
    torch_dtype="auto",
    trust_remote_code=True,
    use_flash_attn=False,
)
model.to('cuda')
model.eval()

def cal_content_similarity(srt_df):
    print(f'开始计算语义相关性：title-text')
    if os.path.exists(f"./Result/title_text_similarity_srt.csv"):
        similarity_df = pd.read_csv(f"./Result/title_text_similarity_srt.csv",encoding='utf-8')
    else:
        similarity_df = pd.DataFrame(columns=['aid','title','title_text_similarity'])
        similarity_df.to_csv(f"./Result/title_text_similarity_srt.csv", index=False,encoding='utf-8')

    pbar = tqdm(total=len(srt_df))
    for index, row in srt_df.iterrows():
        aid = int(row['aid'])
        # 已完成语义相关性计算
        if aid in similarity_df['aid'].values:
            pass
        # 未完成语义相关性计算
        else:
            query = row['title']
            text_list = row['speak_word']
            try:
                documents = eval(text_list)
                sentence_pairs = [[query, doc] for doc in documents]
                scores = model.predict(sentence_pairs, max_length=1024)
                with open(f"./Result/title_text_similarity_srt.csv", 'a+', newline='',encoding='utf-8') as file:
                    writer = csv.writer(file)
                    writer.writerows([[aid,query,scores]])
            except:
                print('error!')
        pbar.update(1)
    pbar.close()

    print('完成计算语义相关性：title-text')

if __name__ == '__main__':

    srt_df = pd.read_csv(f"./Result/srt.csv",encoding='utf-8')
    aid_df = pd.read_csv(f"./List/aid_list.csv",encoding='utf-8')
    srt_df = pd.merge(srt_df,aid_df[['aid','title']],on='aid',how='left')
    cal_content_similarity(srt_df)

