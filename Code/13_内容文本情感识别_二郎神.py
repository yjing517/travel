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
    'http': 'http://127.0.0.1:7899',
    'https': 'http://127.0.0.1:7899'
}

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
print(f"Using device: {device}")

tokenizer=BertTokenizer.from_pretrained('IDEA-CCNL/Erlangshen-Roberta-330M-Sentiment',proxies=proxies,device=device)
model=BertForSequenceClassification.from_pretrained('IDEA-CCNL/Erlangshen-Roberta-330M-Sentiment',proxies=proxies)
model.to(device)
def audio2emo_text(aid_df):
    print(f'开始文本情感识别_text')

    if os.path.exists(f"./Result/text2emo_text.csv"):
        text2emo_text_df = pd.read_csv(f"./Result/text2emo_text.csv",encoding='utf-8')
    else:
        text2emo_text_df = pd.DataFrame(columns=['aid','text_emo_binary'])
        text2emo_text_df.to_csv(f"./Result/text2emo_text.csv", index=False,encoding='utf-8')

    pbar = tqdm(total=len(aid_df))
    for index, row in aid_df.iterrows():
        aid = int(row['aid'])
        audio2emo_result = []
        # 已完成文本情感识别
        if aid in text2emo_text_df['aid'].values:
            pass
        # 未完成文本情感识别
        else:
            text_list = row['speak_word']
            result = []
            if type(text_list) == str:
                for text in eval(text_list):
                    # 对输入文本进行分词
                    inputs = tokenizer(text, return_tensors="pt")
                    # 将输入数据移动到 GPU
                    inputs = {key: value.to(device) for key, value in inputs.items()}
                    # 进行推理
                    with torch.no_grad():
                        outputs = model(**inputs)
                    # 获取预测结果
                    emo_binary = torch.nn.functional.softmax(outputs.logits, dim=-1).tolist()
                    result.append(emo_binary[0])
                audio2emo_result.append([aid,result])
                with open(f"./Result/text2emo_text.csv", 'a+', newline='',encoding='utf-8') as file:
                    writer = csv.writer(file)
                    writer.writerows(audio2emo_result)
        pbar.update(1)
    pbar.close()

    print('文本情感识别完成_text')

if __name__ == '__main__':

    # file_name = f"../List/aid_list.csv"
    file_name = f"./Result/audio2text.csv"
    aid_df = pd.read_csv(file_name,encoding='utf-8')
    audio2emo_text(aid_df)