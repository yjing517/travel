import requests
import pandas as pd
from tqdm import tqdm
import os
import json
import csv
import time
import json

headers = {"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"}
cookies = {
    'SESSDATA': "89af599d%2C1744290621%2C2f856%2Aa1CjAyfXkrFFJWaREqdGyLtJysZ3PZHPeOvaGQ1EOtEEkJWVyg6SoV8prwR8pq-WMOHIoSVkNBMktTRmRYaXlDUS1IY2xLVHRrV25rVDhlejZqZHV0dGdkUXQ3NG1yZDRDeGp4cmVOSkJKa0hUZnhyN2RuSURFZEM3bUFtUTRZSWsyTGRxWjJod3B3IIEC",
    'buvid3':"CC2245B8-7B46-794F-ED69-993CA62030BD64325infoc"
}

def get_ai_subtitle(aid_df):

    if not os.path.exists(f"./List/ai_subtitle.csv"):
        with open(f"./List/ai_subtitle.csv", mode='w', newline='',encoding='utf-8') as file:
            writer = csv.writer(file)
            writer.writerow(['aid', 'cid','subtitle_url','subtitle'])  # 写入表头

    print('开始获取弹幕')
    pbar = tqdm(total=len(aid_df))
    ai_subtitle_df = pd.read_csv(f"./List/ai_subtitle.csv",encoding='utf-8')
    ai_subtitle_df['aid'] = ai_subtitle_df['aid'].astype(int)
    ai_subtitle_aid_list = ai_subtitle_df['aid'].to_list()
    for index, row in aid_df.iterrows():
        aid = int(row['aid'])
        cid = int(row['cid'])
        # 已获取
        if aid in ai_subtitle_aid_list:
            pbar.update(1)
        # 未获取
        else:
            url = 'https://api.bilibili.com/x/player/wbi/v2'
            params = {'aid':aid,'cid':cid}
            response = requests.get(url, params=params, headers=headers,cookies=cookies)
            response.encoding = 'utf-8'
            try:
                subtitle_urls = []
                subtitle_urls = json.loads(response.text)['data']['subtitle']['subtitles']
                if len(subtitle_urls) >1:
                    print(subtitle_urls)
            except:
                print(json.loads(response.text))
                if not json.loads(response.text)['code'] in [-404,-400]:
                    exit()
            # 先只爬取第一份字幕
            if subtitle_urls:
                subtitle_url = subtitle_urls[0]['subtitle_url']
                response = requests.get(f"https:{subtitle_url}",headers=headers,cookies=cookies)
                response.encoding = 'utf-8'
                subtitle = json.loads(response.text)
                pbar.update(1)
                with open(f"./List/ai_subtitle.csv", mode='a', newline='',encoding='utf-8') as file:
                    writer = csv.writer(file)
                    writer.writerow([aid,cid,subtitle_urls,subtitle])
                time.sleep(3)
            else:
                with open(f"./List/ai_subtitle.csv", mode='a', newline='',encoding='utf-8') as file:
                    writer = csv.writer(file)
                    writer.writerow([aid,cid,subtitle_urls,''])
                time.sleep(3)
                
    pbar.close()
    print('AI字幕获取完毕')

if __name__ == '__main__':
    file_name = f"./List/aid_list.csv"
    aid_df = pd.read_csv(file_name,encoding='utf-8')
    get_ai_subtitle(aid_df)
