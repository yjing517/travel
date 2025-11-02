import pandas as pd
import sys
sys.path.append("../..")
import os
import csv
from tqdm import tqdm
import requests
from PIL import Image
from transformers import Blip2Processor, Blip2ForConditionalGeneration

proxies = {
    'http': 'http://127.0.0.1:58648',
    'https': 'http://127.0.0.1:58648'
}

processor = Blip2Processor.from_pretrained("Salesforce/blip2-opt-2.7b",proxies=proxies)
model = Blip2ForConditionalGeneration.from_pretrained("Salesforce/blip2-opt-2.7b",proxies=proxies)
model.to("cuda")  # 将模型移动到GPU

def cover_desc(aid_df):
    print(f'开始封面内容识别')

    if os.path.exists(f"./Result/cover_desc.csv"):
        cover_desc_df = pd.read_csv(f"./Result/cover_desc.csv",encoding='utf-8')
    else:
        cover_desc_df = pd.DataFrame(columns=['aid','cover_desc'])
        cover_desc_df.to_csv(f"./Result/cover_desc.csv", index=False,encoding='utf-8')

    pbar = tqdm(total=len(aid_df))
    for index, row in aid_df.iterrows():
        aid = int(row['aid'])
        cover_desc_result = []
        # 已完成文本情感识别
        if aid in cover_desc_df['aid'].values:
            pass
        # 未完成文本情感识别
        else:
            # 识别标题文本情感
            image_file = f'./Result/Cover/{aid}.jpg'
            if not os.path.exists(image_file):
                image_file = f'./Result/Cover/{aid}.png'
                if not os.path.exists(image_file):
                    continue
            print(image_file)
            raw_image = Image.open(image_file).convert('RGB')
            inputs = processor(raw_image, return_tensors="pt").to("cuda")  # 将输入数据移动到GPU
            out = model.generate(**inputs)
            description = processor.decode(out[0], skip_special_tokens=True)
            print(description)
            exit()
            cover_desc_result.append([aid, description])

            with open(f"./Result/cover_desc.csv", 'a+', newline='',encoding='utf-8') as file:
                writer = csv.writer(file)
                writer.writerows(cover_desc_result)

        pbar.update(1)
    pbar.close()

    print('开始封面内容识别')

if __name__ == '__main__':

    # file_name = f"../List/aid_list.csv"
    file_name = f"./List/aid_list.csv"
    aid_df = pd.read_csv(file_name,encoding='utf-8')
    cover_desc(aid_df)

    # 【消极，积极】