import pandas as pd
import numpy as np
import os
import sys
import csv
sys.path.append("../..")
from tqdm import tqdm
import ast
import xml.etree.ElementTree as ET
# 设置 pandas 显示所有列和行
pd.set_option('display.max_columns', None)  # 显示所有列
pd.set_option('display.max_rows', None)     # 显示所有行
pd.set_option('display.width', None)        # 自动调整列宽
pd.set_option('display.max_colwidth', None) # 显示所有字符

from transformers import AutoModelForSequenceClassification
model = AutoModelForSequenceClassification.from_pretrained(
    'C:/Users/Yuanx/.cache/huggingface/hub/models--jinaai--jina-reranker-v2-base-multilingual/snapshots/6371035883584acb0584c34dbaa9350e4752b8d2',
    torch_dtype="auto",
    trust_remote_code=True,
    use_flash_attn=False,
)
model.to('cuda')
model.eval()

# 解析 XML 字符串
def parse_xml(xml_string):
    root = ET.fromstring(xml_string)
    result = {}
    for child in root:
        if child.tag == 'd':
            # 解析 <d> 标签中的属性
            attributes = child.attrib['p'].split(',')
            content = child.text
            result[child.tag + '_' + str(len(result))] = {
                'attributes': attributes,
                'content': content
            }
        else:
            result[child.tag] = child.text
    return result
# 提取 d 标签中的 content 并存储在列表中
def extract_d_content(parsed_data):
    d_content_list = []
    for key, value in parsed_data.items():
        if key.startswith('d_'):
            d_content_list.append(value['content'])
    return d_content_list
def split_by_length(text, max_length):
    return [text[i:i+max_length] for i in range(0, len(text), max_length)]
def process_danmaku_list(danmaku_list):
    # 将所有元素用空格连接
    combined_text = ','.join(danmaku_list)
    
    # 将连接后的字符串按长度不超过1024分割
    result_list = split_by_length(combined_text, 1024)
    
    return result_list
def subtitle_to_list(subtitle):
    body = subtitle['body']
    return [x['content'] for x in body]
def cal_text_similarity(aid_df,similarity_df,df1,df2):
    print(f"aid_df.shape:{aid_df.shape}")
    print(f"similarity_df.shape:{similarity_df.shape}")
    print(f'开始计算语义相关性')

    pbar = tqdm(total=len(aid_df))
    
    # 标题-封面文字
    df3 = pd.merge(aid_df,df2,how='left',on='aid')
    df3 = df3[['aid','title','cover_text']]

    # 标题-字幕
    # df2 = df2.dropna()
    # df2['subtitle_data'] = df2['subtitle'].apply(ast.literal_eval)
    # df2['subtitle_data'] = df2['subtitle_data'].apply(subtitle_to_list)
    # df3 = pd.merge(aid_df,df2,how='left',on='aid')
    # df3 = df3[['aid','title','subtitle_data']]

    # 标题-评论
    # df2['reply_data'] = df2['reply'].apply(ast.literal_eval)
    # df2['reply_data'] = df2['reply_data'].apply(lambda x: x.get('message'))
    # result = df2.groupby('aid')['reply_data'].agg(list).reset_index()
    # df3 = pd.merge(aid_df,result,how='left',on='aid')
    # df3 = df3[['aid','title','reply_data']]

    # 标题-弹幕
    # df2['danmaku_data'] = df2['danmaku'].apply(parse_xml)
    # df2['danmaku_data'] = df2['danmaku_data'].apply(extract_d_content)
    # df3 = pd.merge(aid_df,df2,how='left',on='aid')
    # df3 = df3[['aid','title','danmaku_data']]

    # 评论-弹幕
    # df1['reply_data'] = df1['reply'].apply(ast.literal_eval)
    # df1['reply_data'] = df1['reply_data'].apply(lambda x: x.get('message'))
    # result = df1.groupby('aid')['reply_data'].agg(list).reset_index()
    # df2['danmaku_data'] = df2['danmaku'].apply(parse_xml)
    # df2['danmaku_data'] = df2['danmaku_data'].apply(extract_d_content)
    # df3 = pd.merge(result,df2,how='left',on='aid')
    # df3 = df3[['aid','reply_data','danmaku_data']]

    for index, row in df3.iterrows():
        aid = int(row['aid'])
        # 已完成计算
        if aid in similarity_df['aid'].values:
            pass
        # 未完成计算
        else:
            # 标题-封面文字
            cover_text = row['cover_text']
            if type(cover_text)==float or not cover_text:
                pass
            else:
                sentence_pairs = [row['title'], cover_text]
                title_cover_text_similarity = model.predict(sentence_pairs, max_length=1024)
                with open(f"./Result/title_cover_text_similarity.csv", 'a+', newline='',encoding='utf-8') as file:
                    writer = csv.writer(file)
                    writer.writerows([[aid,row['title'],cover_text,title_cover_text_similarity]])

            # 标题-字幕
            # subtitle_list = row['subtitle_data']
            # if type(subtitle_list)==float or not subtitle_list:
            #     pass
            # else:
            #     if not type(subtitle_list)==list:
            #         subtitle_list = [subtitle_list]
            #     sentence_pairs = [[row['title'], processed_subtitle] for processed_subtitle in process_danmaku_list(subtitle_list)]
            #     title_subtitle_similarity = model.predict(sentence_pairs, max_length=1024)
            #     len_subtitle = len(subtitle_list)
            #     with open(f"./Result/title_subtitle_similarity.csv", 'a+', newline='',encoding='utf-8') as file:
            #         writer = csv.writer(file)
            #         writer.writerows([[aid,row['title'],title_subtitle_similarity,len_subtitle]])

            # 标题-评论
            # reply_list = row['reply_data']
            # if type(reply_list)==float or not reply_list:
            #     pass
            # else:
            #     if not type(reply_list)==list:
            #         reply_list = [reply_list]
            #     sentence_pairs = [[row['title'], processed_reply] for processed_reply in process_danmaku_list(reply_list)]
            #     title_reply_similarity = model.predict(sentence_pairs, max_length=1024)
            #     len_reply = len(reply_list)
            #     with open(f"./Result/title_reply_similarity.csv", 'a+', newline='',encoding='utf-8') as file:
            #         writer = csv.writer(file)
            #         writer.writerows([[aid,row['title'],title_reply_similarity,len_reply]])

            # 标题-弹幕
            # danmaku_list = row['danmaku_data']
            # if type(danmaku_list)==float or not danmaku_list:
            #     pass
            # else:
            #     if not type(danmaku_list)==list:
            #         danmaku_list = [danmaku_list]
            #     sentence_pairs = [[row['title'], processed_danmaku] for processed_danmaku in process_danmaku_list(danmaku_list)]
            #     title_danmaku_similarity = model.predict(sentence_pairs, max_length=1024)
            #     len_danmaku = len(danmaku_list)
            #     with open(f"./Result/title_danmaku_similarity.csv", 'a+', newline='',encoding='utf-8') as file:
            #         writer = csv.writer(file)
            #         writer.writerows([[aid,row['title'],title_danmaku_similarity,len_danmaku]])
                
            # 评论-弹幕
            # reply_list = row['reply_data']
            # danmaku_list = row['danmaku_data']
            # if type(reply_list)==float or not reply_list:
            #     pass
            # if type(danmaku_list)==float or not danmaku_list:
            #     pass
            # else:
            #     if not type(reply_list)==list:
            #         reply_list = [reply_list]
            #     if not type(danmaku_list)==list:
            #         danmaku_list = [danmaku_list]
            #     sentence_pairs = []
            #     for reply in process_danmaku_list(reply_list):
            #         for danmaku in process_danmaku_list(danmaku_list):
            #             sentence_pairs.append([reply,danmaku])
            #     reply_danmaku_similarity = model.predict(sentence_pairs, max_length=1024)
            #     with open(f"./Result/reply_danmaku_similarity.csv", 'a+', newline='',encoding='utf-8') as file:
            #         writer = csv.writer(file)
            #         writer.writerows([[aid,reply_danmaku_similarity]])

        pbar.update(1)
    pbar.close()

    print('完成计算语义相关性：title-text')

if __name__ == '__main__':

    aid_df = pd.read_csv(f"./List/aid_list.csv",encoding='utf-8')

    # danmaku_df['danmaku2'] = danmaku_df['danmaku'].apply(lambda x:len(x))
    # print(danmaku_df['danmaku2'].value_counts().head(10))

    # 标题-封面文字
    if os.path.exists(f"./Result/title_covertext_similarity.csv"):
        similarity_df = pd.read_csv(f"./Result/title_covertext_similarity.csv",encoding='utf-8')
    else:
        similarity_df = pd.DataFrame(columns=['aid','title','cover_text','title_covertext_similarity'])
        similarity_df.to_csv(f"./Result/title_covertext_similarity.csv", index=False,encoding='utf-8')
    covertext_df = pd.read_csv(f"./Result/cover_text.csv",encoding='utf-8')
    cal_text_similarity(aid_df,similarity_df,'',covertext_df)

    # 标题-字幕
    # if os.path.exists(f"./Result/title_subtitle_similarity.csv"):
    #     similarity_df = pd.read_csv(f"./Result/title_subtitle_similarity.csv",encoding='utf-8')
    # else:
    #     similarity_df = pd.DataFrame(columns=['aid','title','title_subtitle_similarity','len_reply'])
    #     similarity_df.to_csv(f"./Result/title_subtitle_similarity.csv", index=False,encoding='utf-8')
    # subtitle_df = pd.read_csv(f"./List/ai_subtitle.csv",encoding='utf-8')
    # cal_text_similarity(aid_df,similarity_df,'',subtitle_df)

    # 标题-评论
    # if os.path.exists(f"./Result/title_reply_similarity.csv"):
    #     similarity_df = pd.read_csv(f"./Result/title_reply_similarity.csv",encoding='utf-8')
    # else:
    #     similarity_df = pd.DataFrame(columns=['aid','title','title_reply_similarity','len_reply'])
    #     similarity_df.to_csv(f"./Result/title_reply_similarity.csv", index=False,encoding='utf-8')
    # reply_df = pd.read_csv(f"./List/reply.csv",encoding='utf-8')
    # cal_text_similarity(aid_df,similarity_df,'',reply_df)

    # 标题-弹幕
    # if os.path.exists(f"./Result/title_danmaku_similarity.csv"):
    #     similarity_df = pd.read_csv(f"./Result/title_danmaku_similarity.csv",encoding='utf-8')
    # else:
    #     similarity_df = pd.DataFrame(columns=['aid','title','title_danmaku_similarity','len_danmaku'])
    #     similarity_df.to_csv(f"./Result/title_danmaku_similarity.csv", index=False,encoding='utf-8')
    # danmaku_df = pd.read_csv(f"./List/danmaku.csv",encoding='utf-8')
    # cal_text_similarity(aid_df,similarity_df,'',danmaku_df)

    # 评论-弹幕
    # if os.path.exists(f"./Result/reply_danmaku_similarity.csv"):
    #     similarity_df = pd.read_csv(f"./Result/reply_danmaku_similarity.csv",encoding='utf-8')
    # else:
    #     similarity_df = pd.DataFrame(columns=['aid','title','reply_danmaku_similarity'])
    #     similarity_df.to_csv(f"./Result/reply_danmaku_similarity.csv", index=False,encoding='utf-8')
    # reply_df = pd.read_csv(f"./List/reply.csv",encoding='utf-8')
    # danmaku_df = pd.read_csv(f"./List/danmaku.csv",encoding='utf-8')
    # cal_text_similarity(aid_df,similarity_df,reply_df,danmaku_df)




