import time

import requests
import json
import os
import datetime
from tqdm import tqdm
import pandas as pd

headers={"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"}

def get_id_list(file_name=f"../List/aid_list_new_craw.csv",rid=0,num=10,max_duration=600):
    '''
        num: 爬取的aid个数
    '''

    print(f'开始爬取视频aid,爬取次数:{num},rid:{rid}')
    # pbar = tqdm(total=num)

    for n in range(num):

        # 读取已经爬取的aid号
        file_name = file_name
        if os.path.exists(file_name):
            aid_df = pd.read_csv(file_name)
        else:
            aid_df = pd.DataFrame(columns=['aid'])
        aid_list = aid_df['aid'].values
        aid_list = [int(float(aid)) for aid in aid_list]

        # 设置要爬取的url
        url = f'https://api.bilibili.com/x/web-interface/dynamic/region?ps=50&pn=1&rid={rid}'
        response = requests.get(url, headers=headers, )
        # print(response)
        data_json = json.loads(response.text)

        counter = 0
        for i in data_json['data']['archives']:

            # 判断该视频是否已经爬取
            aid = int(i['aid'])

            if aid not in aid_list and aid not in aid_all:
                new_data_aid = {}
                new_data_aid['aid'] = aid
            else:
                counter += 1
                continue

            # 视频封面图片url
            new_data_aid['cover_url'] = i['pic']
            # 视频标题
            new_data_aid['title'] = i['title']
            # 发布日期
            new_data_aid['pubdate'] = i['pubdate']
            # 视频描述
            new_data_aid['desc'] = i['desc']
            try:
                # tid -> 1615271
                new_data_aid['tid'] = i['tid']
                # tname,视频标签 -> 米哈游
                new_data_aid['tname'] = i['tname']
            except KeyError:
                new_data_aid['tid'] = '-'
                new_data_aid['tname'] = '-'
            # UP主mid
            new_data_aid['mid'] = i['owner']['mid']
            # 视频长度 -> 901
            new_data_aid['duration'] = i['duration']
            try:
                # 发布IP -> 广东
                new_data_aid['pub_location'] = i['pub_location']
            except:
                new_data_aid['pub_location'] = '-'
            # bvid -> BV1z4YMeAE1S
            new_data_aid['bvid'] = i['bvid']
            # aid爬取时间
            new_data_aid['aid爬取时间'] = datetime.datetime.now()

            # 只要视频时长小于1200s的视频
            if new_data_aid['duration'] < max_duration:
                aid_df = pd.concat([aid_df, pd.DataFrame([new_data_aid])], ignore_index=True)

        print(len(data_json['data']['archives'])-counter)
        pbar.update(1)

        # 保存id信息
        aid_df.to_csv(file_name, encoding='utf-8', index=False)
        time.sleep(1)
        clean_aid_df(file_name)

    # pbar.close()

    print('完成视频aid爬取')

def clean_aid_df(file_name):

    file_name = file_name
    aid_df = pd.read_csv(file_name)
    # print(aid_df.shape)

    aid_df = aid_df.dropna(subset=['aid爬取时间'])
    aid_df.drop_duplicates(subset=['aid'], inplace=True)  # 去除第一列的重复项

    # print(aid_df.shape)
    aid_df.to_csv(file_name, encoding='utf-8', index=False)

if __name__ == '__main__':

    file_name = f"List/aid_list.csv"

    # 之前爬去过的csv
    aid_all = []

    # 所有视频分区
    rid_list = [250]

    while 1:
        num = 10
        pbar = tqdm(total=len(rid_list)*num)
        for rid in rid_list:
            # 爬取 num 个 id, 视频最大长度为 max_duration
            get_id_list(file_name=file_name,rid=rid,num=num,max_duration=1800)
        pbar.close()
