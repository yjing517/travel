import requests
import pandas as pd
from tqdm import tqdm
import os
import json
import csv
import time

headers = {"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"}
cookies = {
    # 'SESSDATA': '89af599d%2C1744290621%2C2f856%2Aa1CjAyfXkrFFJWaREqdGyLtJysZ3PZHPeOvaGQ1EOtEEkJWVyg6SoV8prwR8pq-WMOHIoSVkNBMktTRmRYaXlDUS1IY2xLVHRrV25rVDhlejZqZHV0dGdkUXQ3NG1yZDRDeGp4cmVOSkJKa0hUZnhyN2RuSURFZEM3bUFtUTRZSWsyTGRxWjJod3B3IIEC'
    'SESSDATA': '7a0465f5%2C1767076200%2Ce868b%2A71CjB2e7i1s3ikQcNZCT5sgPjHIPxNBx-8RND6aGe2BLCYU8XewYMWES3Z4T4iGgBie4YSVlREcktqdGczRmNTR1VtaTNFSl9OQWRENFNDdHJrMWVXUElOYVJGeldnS3VEQk03VEdSOFE3azNwNENaaXdVRUYxOVZ4ZHAwcnVDQ3FYZ0FYUHRQdWxBIIEC'
}
def get_reply(aid_df):

    if not os.path.exists(f"List/reply.csv"):
        with open(f"List/reply.csv", mode='w', newline='',encoding='utf-8-sig') as file:
            writer = csv.writer(file)
            writer.writerow(['aid', 'reply'])  # 写入表头

    print('开始获取评论')
    pbar = tqdm(total=len(aid_df))
    reply_df = pd.read_csv(f"List/reply.csv",encoding='utf-8')
    reply_df['aid'] = reply_df['aid'].astype(int)
    reply_aid_list = list(set(reply_df['aid'].to_list()))
    for index, row in aid_df[aid_df['reply'] != 0].iterrows():
        aid = int(row['aid'])
        # 已获取
        if aid in reply_aid_list:
            pbar.update(1)
        # 未获取
        else:
            try:
                url = 'https://api.bilibili.com/x/v2/reply'
                # print(aid)
                params = {'type':1,'oid':aid,
                        'sort':1, # 按照点赞数排序
                        'nohot':0,
                        'ps':20, # 20条一页
                        'pn':1 # 第n页
                        }
                response = requests.get(url, params=params, headers=headers,cookies=cookies)
                data_json = json.loads(response.text)
                reply_count = data_json['data']['page']['acount']
                # print(reply_count)
                reply_list = []
                if reply_count == 0:
                    continue
                
                for n in range(1,min(5,reply_count//20+1)): # 点赞数最多的前1000条
                    params = {'type':1,'oid':aid,'sort':1,'nohot':0,'ps':20,'pn':n}
                    response = requests.get(url, params=params, headers=headers,cookies=cookies)
                    data_json = json.loads(response.text)
                    data = data_json['data']
                    replies = data['replies']
                    if not replies:
                        break
                    for reply in replies:
                        data_dict = {'rpid':reply['rpid'],
                                    'oid':reply['rpid'],
                                    'mid':reply['mid'],
                                    'count':reply['count'],
                                    'rcount':reply['rcount'],
                                    'ctime':reply['ctime'],
                                    'like':reply['like'],
                                    'message':reply['content']['message'],
                                    }
                        reply_list.append([aid,data_dict])
                pbar.update(1)
                with open(f"List/reply.csv", mode='a', newline='',encoding='utf-8-sig') as file:
                    writer = csv.writer(file)
                    writer.writerows(reply_list)
                time.sleep(5)
            except:
                print(data_json)
    pbar.close()
    print('评论获取完毕')


if __name__ == '__main__':
    file_name = f"List/aid_list.csv"
    aid_df = pd.read_csv(file_name,encoding='utf-8')
    get_reply(aid_df)
