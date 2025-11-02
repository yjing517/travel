import requests
import json
import datetime
from tqdm import tqdm
import pandas as pd
import numpy as np

headers = {"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"}

# 需要 覆盖/新添 数据的列名
col_list = ['bvid', 'cover_url', 'tid', 'tname', 'pubdate', 'ctime', 'desc', 'desc_v2', 'state', 'mission_id', 'view', 'danmaku', 'reply',
            'favorite', 'coin', 'share', 'like', 'argue_info', 'cid', 'dimension', 'honor_reply', 'participle', 'sex',
            'face', 'fans', 'friend', 'sign', 'current_level', 'Official', 'official_verify', 'vip', 'is_senior_member',
            'archive_count', 'article_count', 'like_num', 'Tags', '视频信息爬取时间']

def get_video_info(row):
    aid = row['aid']
    get_video_info_time = row['视频信息爬取时间']

    # 如果这个aid的视频信息还未爬取
    if pd.isna(get_video_info_time):
        # 设置要爬取的url
        url = 'https://api.bilibili.com/x/web-interface/view/detail'
        params = {'aid': aid}
        response = requests.get(url, params=params, headers=headers)
        data_json = json.loads(response.text)
        try:
            data = data_json['data']
        except:
            print(data_json)
            print(f"{aid}:keyerror")
            pbar.update(1)
            return [None] * len(col_list)

        video_info = {key: None for key in col_list}

        #####################    视频基本信息    #####################

        data_view = data['View']

        # 封面图片地址
        video_info['cover_url'] = data_view['pic']
        # tid
        video_info['tid'] = data_view['tid']
        # tname
        video_info['tname'] = data_view['tname']
        # BV号 -> BV1Hy411B7m9
        video_info['bvid'] = data_view['bvid']
        # 发布时间 -> 1721019600
        video_info['pubdate'] = data_view['pubdate']
        # 投稿时间 -> 1720874819
        video_info['ctime'] = data_view['ctime']
        # 视频简介 -> 一切都是最好的安排~
        video_info['desc'] = data_view['desc']
        # 新版视频简介 -> 一切都是最好的安排~
        video_info['desc_v2'] = data_view['desc_v2']
        # 视频状态 -> 0
        video_info['state'] = data_view['state']
        # 稿件参与的活动id -> 4017418
        if 'mission_id' in data_view:
            video_info['mission_id'] = data_view['mission_id']
        else:
            video_info['mission_id'] = 0
        # 播放量 -> 305362
        video_info['view'] = data_view['stat']['view']
        # 弹幕量 -> 640
        video_info['danmaku'] = data_view['stat']['danmaku']
        # 评论量 -> 856
        video_info['reply'] = data_view['stat']['reply']
        # 收藏量 -> 2013
        video_info['favorite'] = data_view['stat']['favorite']
        # 投币量 -> 4055
        video_info['coin'] = data_view['stat']['coin']
        # 分享量 -> 1397
        video_info['share'] = data_view['stat']['share']
        # 点赞量 -> 13493
        video_info['like'] = data_view['stat']['like']
        # 警告提醒 -> 该内容疑似使用AI技术合成，请谨慎甄别
        video_info['argue_info'] = data_view['argue_info']
        # cid -> 1615862368
        video_info['cid'] = data_view['cid']
        # 视频分辨率 -> {"width": 3840,"height": 2160,"rotate": 0}
        video_info['dimension'] = data_view['dimension']
        # honor_reply
        video_info['honor_reply'] = data_view['honor_reply']
        # 内容关键词
        video_info['participle'] = data['participle']

        #####################    UP主信息    #####################

        data_Card = data['Card']
        # 性别 -> 男/女/保密
        video_info['sex'] = data_Card['card']['sex']
        # 头像链接 -> https://face.jpg
        video_info['face'] = data_Card['card']['face']
        # 粉丝量 -> 12345
        video_info['fans'] = data_Card['card']['fans']
        # UP主关注量 -> 10
        video_info['friend'] = data_Card['card']['friend']
        # 签名 -> 我的weixin:xxx,email:xxx
        video_info['sign'] = data_Card['card']['sign']
        # 等级 -> 6
        video_info['current_level'] = data_Card['card']['level_info']['current_level']
        # 认证信息 -> 大V / bilibili 知名科技UP主
        video_info['Official'] = data_Card['card']['Official']
        video_info['official_verify'] = data_Card['card']['official_verify']
        # 大会员状态 -> 1
        video_info['vip'] = data_Card['card']['vip']
        # 是否为硬核会员 -> 0
        video_info['is_senior_member'] = data_Card['card']['is_senior_member']
        # 用户稿件数量 -> 417
        video_info['archive_count'] = data_Card['archive_count']
        # 用户专栏数量 -> 0
        video_info['article_count'] = data_Card['article_count']
        # UP主获赞数
        video_info['like_num'] = data_Card['like_num']

        #####################    视频TAG信息    #####################

        data_Tags = data['Tags']
        # 全部Tags信息
        video_info['Tags'] = data_Tags
        # tag_id,bgm,music_id,tag_name,tag_type
        # tag0好像是B站自动识别的bgm or 场景声音

        video_info['视频信息爬取时间'] = datetime.datetime.now().timestamp()
        pbar.update(1)
        # print(video_info)
        result_list = [video_info[key] for key in col_list]
        if len(result_list) != 37:
            print(aid)
            print(len(result_list))
        return result_list

    # 如果这个aid的视频信息已经爬取
    else:
        pbar.update(1)
        return row[col_list].tolist()

if __name__ == '__main__':
    file_name = f"List/aid_list.csv"
    aid_df = pd.read_csv(file_name)
    aid_df['aid'].astype(int)
    print('开始获取视频信息')
    pbar = tqdm(total=len(aid_df))


    # 第一次爬视频信息
    if '视频信息爬取时间' not in aid_df.columns:
        aid_df['视频信息爬取时间'] = pd.NA

    # 计数器
    count = 0
    error_count = 0
    for index, row in aid_df.iterrows():

        # try:
        aid_df.loc[index, col_list] = np.array(get_video_info(row), dtype=object)
        # except Exception as e:
        #     error_count += 1
        count += 1

        # 每爬取100行保存一次
        if count % 1000 == 0:
            aid_df.to_csv(file_name, encoding='utf-8', index=False)
            print(f"已保存前 {count} 行数据")

    # 保存最后的数据
    aid_df.to_csv(file_name, encoding='utf-8', index=False)

    pbar.close()
    print('完成视频信息爬取')
    print(f"error_count:{error_count}")