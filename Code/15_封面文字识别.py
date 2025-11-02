import pandas as pd
import sys
sys.path.append("../..")
import os
import csv
from tqdm import tqdm
import torch
from transformers import AutoModel, AutoTokenizer

proxies = {
    'http': 'http://127.0.0.1:58648',
    'https': 'http://127.0.0.1:58648'
}

tokenizer = AutoTokenizer.from_pretrained('ucaslcl/GOT-OCR2_0', trust_remote_code=True,proxies=proxies)
model = AutoModel.from_pretrained('ucaslcl/GOT-OCR2_0', trust_remote_code=True, low_cpu_mem_usage=True, device_map='cuda', use_safetensors=True, pad_token_id=tokenizer.eos_token_id,proxies=proxies)
model = model.eval().cuda()

def cover_text(aid_df):
    print(f'开始封面文字识别')

    if os.path.exists(f"./Result/cover_text.csv"):
        cover_text_df = pd.read_csv(f"./Result/cover_text.csv",encoding='utf-8')
    else:
        cover_text_df = pd.DataFrame(columns=['aid','cover_text'])
        cover_text_df.to_csv(f"./Result/cover_text.csv", index=False,encoding='utf-8')

    pbar = tqdm(total=len(aid_df))
    for index, row in aid_df.iterrows():
        aid = int(row['aid'])
        cover_text_result = []
        # 已完成文本情感识别
        if aid in cover_text_df['aid'].values:
            pass
        # 未完成文本情感识别
        else:
            # 识别标题文本情感
            image_file = f'./Result/Cover/{aid}.jpg'
            if not os.path.exists(image_file):
                image_file = f'./Result/Cover/{aid}.png'
                if not os.path.exists(image_file):
                    continue
            res = model.chat(tokenizer, image_file, ocr_type='ocr')
            cover_text_result.append([aid,res])
            with open(f"./Result/cover_text.csv", 'a+', newline='',encoding='utf-8') as file:
                writer = csv.writer(file)
                writer.writerows(cover_text_result)

        pbar.update(1)
    pbar.close()

    print('封面文字识别完成')

if __name__ == '__main__':

    # file_name = f"../List/aid_list.csv"
    file_name = f"./List/aid_list.csv"
    aid_df = pd.read_csv(file_name,encoding='utf-8')
    cover_text(aid_df)

    # 【消极，积极】