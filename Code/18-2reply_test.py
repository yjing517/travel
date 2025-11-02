import requests
import pandas as pd
from tqdm import tqdm
import os
import json
import csv
import time

headers = {"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"}
cookies = {
    'SESSDATA': '7a0465f5%2C1767076200%2Ce868b%2A71CjB2e7i1s3ikQcNZCT5sgPjHIPxNBx-8RND6aGe2BLCYU8XewYMWES3Z4T4iGgBie4YSVlREcktqdGczRmNTR1VtaTNFSl9OQWRENFNDdHJrMWVXUElOYVJGeldnS3VEQk03VEdSOFE3azNwNENaaXdVRUYxOVZ4ZHAwcnVDQ3FYZ0FYUHRQdWxBIIEC'
}

aid = 2
url = 'https://api.bilibili.com/x/v2/reply'
params = {'type':1,'oid':aid,
        'sort':1, # 按照点赞数排序
        'nohot':0,
        'ps':10, # 20条一页
        'pn':1 # 第n页
        }
response = requests.get(url, params=params, headers=headers,cookies=cookies)
data_json = json.loads(response.text)
reply_count = data_json['data']['page']['acount']
print(reply_count)
data = data_json['data']
replies = data['replies']
reply_list = []
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

print(reply_list)