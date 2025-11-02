import requests
from PIL import Image
from io import BytesIO
import pandas as pd
from tqdm import tqdm
import os

def get_cover(aid_df):
    print('开始获取视频封面')
    pbar = tqdm(total=len(aid_df))
    for index, row in aid_df.iterrows():
        aid = int(row['aid'])
        # 已获取视频封面
        if os.path.exists(f"Result/Cover/{aid}.jpg") or os.path.exists(f"Result/Cover/{aid}.png"):
            pbar.update(1)
        # 未获取视频封面
        else:
            img = Image.open(BytesIO(requests.get(row['cover_url']).content))
            try:
                img.save(f"Result/Cover/{aid}.jpg",format='JPEG')
            except:
                img.save(f"Result/Cover/{aid}.png", format='PNG')
            pbar.update(1)
    pbar.close()
    print('视频封面获取完毕')

if __name__ == '__main__':
    file_name = f"List/aid_list.csv"
    aid_df = pd.read_csv(file_name,encoding='utf-8')
    get_cover(aid_df)
