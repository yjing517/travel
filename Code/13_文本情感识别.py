import pandas as pd
import sys
sys.path.append("../..")
import os
import csv
from tqdm import tqdm
import torch

from transformers import BertForSequenceClassification
from transformers import BertTokenizer
tokenizer = BertTokenizer.from_pretrained("C:/Users/Yuanx/.cache/huggingface/hub/models--IDEA-CCNL--Erlangshen-Roberta-330M-Sentiment/snapshots/7005a53278f557cb27010fb08bb56a88b92173a9",
                                          torch_dtype="auto",
                                          trust_remote_code=True,
                                          use_flash_attn=False)
model = BertForSequenceClassification.from_pretrained("C:/Users/Yuanx/.cache/huggingface/hub/models--IDEA-CCNL--Erlangshen-Roberta-330M-Sentiment/snapshots/7005a53278f557cb27010fb08bb56a88b92173a9",
                                          torch_dtype="auto",
                                          trust_remote_code=True,
                                          use_flash_attn=False)
# 将模型移动到GPU
model.to('cuda')
model.eval()

# # 设置代理
# proxies = {
#     'http': 'http://127.0.0.1:58648',
#     'https': 'http://127.0.0.1:58648'
# }
# # 加载预训练的BERT模型和分词器
# tokenizer = BertTokenizer.from_pretrained('IDEA-CCNL/Erlangshen-Roberta-330M-Sentiment', proxies=proxies)
# model = BertForSequenceClassification.from_pretrained('IDEA-CCNL/Erlangshen-Roberta-330M-Sentiment', proxies=proxies)

def cal_emo_binary(aid_df,emo_df,df1):
    print(f'开始文本情感识别_title')                            

    pbar = tqdm(total=len(aid_df))

    for index, row in aid_df.iterrows():
        aid = int(row['aid'])
        # 已完成文本情感识别
        if aid in emo_df['aid'].values:
            pass
        # 未完成文本情感识别
        else:
            # 标题
            # inputs = tokenizer.encode(row['title'], return_tensors='pt').to('cuda')  # 将输入数据移动到GPU
            # with torch.no_grad():
            #     output = model(inputs)
            # emo_binary = torch.nn.functional.softmax(output.logits, dim=-1).tolist()[0]
            # with open(f"./Result/emo/title_emo.csv", 'a+', newline='', encoding='utf-8') as file:
            #     writer = csv.writer(file)
            #     writer.writerow([aid, row['title'], emo_binary])
            # 封面图片


            
            inputs = tokenizer.encode(row['title'], return_tensors='pt').to('cuda')  # 将输入数据移动到GPU
            with torch.no_grad():
                output = model(inputs)
            emo_binary = torch.nn.functional.softmax(output.logits, dim=-1).tolist()[0]
            with open(f"./Result/emo/title_emo.csv", 'a+', newline='', encoding='utf-8') as file:
                writer = csv.writer(file)
                writer.writerow([aid, row['title'], emo_binary])


        pbar.update(1)
    pbar.close()

    print('文本情感识别完成_title')

if __name__ == '__main__':
    file_name = f"./List/aid_list.csv"
    aid_df = pd.read_csv(file_name, encoding='utf-8')

    # 标题
    # if os.path.exists(f"./Result/emo/title_emo.csv"):
    #     emo_df = pd.read_csv(f"./Result/emo/title_emo.csv",encoding='utf-8')
    # else:
    #     emo_df = pd.DataFrame(columns=['aid','title','title_emo_binary'])
    #     emo_df.to_csv(f"./Result/emo/title_emo.csv", index=False,encoding='utf-8')
    # title_df = pd.read_csv(f"./Result/emo/title_emo.csv",encoding='utf-8')
    # cal_emo_binary(aid_df,emo_df,aid_df)

    # 封面文字
    if os.path.exists(f"./Result/emo/covertext_emo.csv"):
        emo_df = pd.read_csv(f"./Result/emo/covertext_emo.csv",encoding='utf-8')
    else:
        emo_df = pd.DataFrame(columns=['aid','covertext','covertext_emo_binary'])
        emo_df.to_csv(f"./Result/emo/covertext_emo.csv", index=False,encoding='utf-8')
    covertext_df = pd.read_csv(f"./Result/emo/covertext_emo.csv",encoding='utf-8')
    cal_emo_binary(aid_df,emo_df,covertext_df)
