import pandas as pd
import sys
sys.path.append("../..")
import os
import csv
from tqdm import tqdm

from transformers import BertForSequenceClassification
from transformers import BertTokenizer
import torch

proxies = {
    'http': 'http://127.0.0.1:7897',
    'https': 'http://127.0.0.1:7897'
}

tokenizer=BertTokenizer.from_pretrained('IDEA-CCNL/Erlangshen-Roberta-330M-Sentiment',proxies=proxies)
model=BertForSequenceClassification.from_pretrained('IDEA-CCNL/Erlangshen-Roberta-330M-Sentiment',proxies=proxies)
def text2emo_cover_text(aid_df):
    print(f'开始文本情感识别_cover_text')

    if os.path.exists(f"./Result/text2emo_cover_text.csv"):
        text2emo_cover_text_df = pd.read_csv(f"./Result/text2emo_cover_text.csv",encoding='utf-8')
    else:
        text2emo_cover_text_df = pd.DataFrame(columns=['aid','cover_text','cover_text_emo_binary'])
        text2emo_cover_text_df.to_csv(f"./Result/text2emo_cover_text.csv", index=False,encoding='utf-8')

    pbar = tqdm(total=len(aid_df))
    for index, row in aid_df.iterrows():
        aid = int(row['aid'])
        audio2emo_result = []
        # 已完成文本情感识别
        if aid in text2emo_cover_text_df['aid'].values:
            pass
        # 未完成文本情感识别
        else:
            # 识别标题文本情感
            cover_text = row['cover_text']
            output=model(torch.tensor([tokenizer.encode(cover_text)]))
            emo_binary = torch.nn.functional.softmax(output.logits,dim=-1).tolist()
            audio2emo_result.append([aid,cover_text,emo_binary])
            with open(f"./Result/text2emo_cover_text.csv", 'a+', newline='',encoding='utf-8') as file:
                writer = csv.writer(file)
                writer.writerows(audio2emo_result)

        pbar.update(1)
    pbar.close()

    print('文本情感识别完成_cover_text')

if __name__ == '__main__':

    # file_name = f"../List/aid_list.csv"
    file_name = f"./Result/cover_text.csv"
    aid_df = pd.read_csv(file_name,encoding='utf-8')
    text2emo_cover_text(aid_df)

    # 【消极，积极】