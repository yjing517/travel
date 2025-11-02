import pandas as pd
import sys
sys.path.append("../..")
import os
import csv
from tqdm import tqdm
import ast

# from transformers import BertForSequenceClassification
# from transformers import BertTokenizer
# import torch

# proxies = {
#     'http': 'http://127.0.0.1:7899',
#     'https': 'http://127.0.0.1:7899'
# }

# device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
# print(f"Using device: {device}")

# tokenizer=BertTokenizer.from_pretrained('IDEA-CCNL/Erlangshen-Roberta-330M-Sentiment',proxies=proxies,device=device)
# model=BertForSequenceClassification.from_pretrained('IDEA-CCNL/Erlangshen-Roberta-330M-Sentiment',proxies=proxies)
# model.to(device)

def emo_recognize(reply_df,reply_emo_df):
    print(f'开始文本情感识别')
    pbar = tqdm(total=len(reply_df))

    # reply_df['reply'] = reply_df['reply'].apply(ast.literal_eval)
    reply_df['danmaku'] = reply_df['danmaku'].apply(ast.literal_eval)

    for index, row in reply_df.iterrows():
        aid = int(row['aid'])
        # 已完成文本情感识别
        if aid in reply_emo_df['aid'].values:
            pass
        # 未完成文本情感识别
        else:
            # reply_list = reply_df[reply_df['aid']==aid]['reply'].apply(lambda x: x.get('message')).tolist()
            print(reply_df[reply_df['aid']==aid]['reply'])

            exit()
            result = []
            if reply_list:
                for reply in reply_list:
                    # 对输入文本进行分词
                    inputs = tokenizer(reply, return_tensors="pt")
                    # 将输入数据移动到 GPU
                    inputs = {key: value.to(device) for key, value in inputs.items()}
                    # 进行推理
                    with torch.no_grad():
                        outputs = model(**inputs)
                    # 获取预测结果
                    emo_binary = torch.nn.functional.softmax(outputs.logits, dim=-1).tolist()
                    result.append(emo_binary[0])
            print(result)
            exit()
                # with open(f"./Result/reply_emo.csv", 'a+', newline='',encoding='utf-8') as file:
                #     writer = csv.writer(file)
                #     writer.writerow([aid,result])
        pbar.update(1)
    pbar.close()

    print('文本情感识别完成')

if __name__ == '__main__':

    # 评论
    # if not os.path.exists(f"./Result/reply_emo.csv"):
    #     reply_emo_df = pd.DataFrame(columns=['aid','emo_binary'])
    #     reply_emo_df.to_csv(f"./Result/reply_emo.csv", index=False,encoding='utf-8')
    # reply_emo_df = pd.read_csv(f"./Result/reply_emo.csv",encoding='utf-8')
    # reply_df = pd.read_csv(f"./List/reply.csv",encoding='utf-8')
    # emo_recognize(reply_df,reply_emo_df)

    # 弹幕
    if not os.path.exists(f"./Result/danmaku_emo.csv"):
        danmaku_emo_df = pd.DataFrame(columns=['aid','emo_binary'])
        danmaku_emo_df.to_csv(f"./Result/danmaku_emo.csv", index=False,encoding='utf-8')
    danmaku_emo_df = pd.read_csv(f"./Result/danmaku_emo.csv",encoding='utf-8')
    danmaku_df = pd.read_csv(f"./List/danmaku.csv",encoding='utf-8')
    emo_recognize(danmaku_df,danmaku_emo_df)