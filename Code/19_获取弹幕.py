import requests
import pandas as pd
from tqdm import tqdm
import os
import json
import csv
import time


headers = {"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"}
cookies = {
    'SESSDATA': '89af599d%2C1744290621%2C2f856%2Aa1CjAyfXkrFFJWaREqdGyLtJysZ3PZHPeOvaGQ1EOtEEkJWVyg6SoV8prwR8pq-WMOHIoSVkNBMktTRmRYaXlDUS1IY2xLVHRrV25rVDhlejZqZHV0dGdkUXQ3NG1yZDRDeGp4cmVOSkJKa0hUZnhyN2RuSURFZEM3bUFtUTRZSWsyTGRxWjJod3B3IIEC'
}
def get_danmaku(aid_df):

    if not os.path.exists(f"List/danmaku.csv"):
        with open(f"List/danmaku.csv", mode='w', newline='',encoding='utf-8') as file:
            writer = csv.writer(file)
            writer.writerow(['aid', 'cid','danmaku'])  # 写入表头

    print('开始获取弹幕')
    pbar = tqdm(total=len(aid_df))
    danmaku_df = pd.read_csv(f"List/danmaku.csv",encoding='utf-8')
    danmaku_df['aid'] = danmaku_df['aid'].astype(int)
    danmaku_aid_list = danmaku_df['aid'].to_list()
    for index, row in aid_df[aid_df['danmaku'] != 0].iterrows():
        aid = int(row['aid'])
        cid = int(row['cid'])
        # 已获取
        if aid in danmaku_aid_list:
            pbar.update(1)
        # 未获取
        else:
            url = 'https://api.bilibili.com/x/v1/dm/list.so'
            params = {'oid':cid}
            response = requests.get(url, params=params, headers=headers,cookies=cookies)
            response.encoding = 'utf-8'
            pbar.update(1)
            with open(f"List/danmaku.csv", mode='a', newline='',encoding='utf-8') as file:
                writer = csv.writer(file)
                writer.writerow([aid,cid,response.text])
            time.sleep(3)
    pbar.close()
    print('弹幕获取完毕')

if __name__ == '__main__':
    file_name = f"List/aid_list.csv"
    aid_df = pd.read_csv(file_name,encoding='utf-8')
    get_danmaku(aid_df)
