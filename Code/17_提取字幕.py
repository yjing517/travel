import re
import pandas as pd
import sys
sys.path.append("../..")
import os
import csv
from tqdm import tqdm
import string
# 设置 pandas 显示所有列和行
pd.set_option('display.max_columns', None)  # 显示所有列
pd.set_option('display.max_rows', None)     # 显示所有行
pd.set_option('display.width', None)        # 自动调整列宽
pd.set_option('display.max_colwidth', None) # 显示所有字符

def read_srt(file_name):
    srt_data = []
    with open(file_name, 'r', encoding='utf-8') as file:
        lines = file.readlines()

    i = 0
    while i < len(lines):
        # 读取序号
        if re.match(r'^\d+$', lines[i].strip()):
            index = int(lines[i].strip())
            i += 1
        else:
            i += 1
            continue

        # 读取时间戳
        if re.match(r'^\d{2}:\d{2}:\d{2},\d{3} --> \d{2}:\d{2}:\d{2},\d{3}$', lines[i].strip()):
            times = lines[i].strip().split(' --> ')
            start_time = times[0]
            end_time = times[1]
            i += 1
        else:
            i += 1
            continue

        # 读取文本内容
        text = []
        while i < len(lines) and lines[i].strip() != '':
            text.append(lines[i].strip())
            i += 1

        # 将解析结果添加到列表中
        srt_data.append({
            'index': index,
            'start_time': start_time,
            'end_time': end_time,
            'text': ' '.join(text)
        })
    return srt_data

def get_srt(aid_df):
    print(f'开始提取字幕')

    if os.path.exists(f"Result/srt.csv"):
        srt_df = pd.read_csv(f"Result/srt.csv",encoding='utf-8')
    else:
        srt_df = pd.DataFrame(columns=['aid','srt'])
        srt_df.to_csv(f"Result/srt.csv", index=False,encoding='utf-8')

    pbar = tqdm(total=len(aid_df))
    for index, row in aid_df.iterrows():
        aid = int(row['aid'])
        srt_result = []
        # 已完成字幕提取
        if aid in srt_df['aid'].values:
            pbar.update(1)
        # 未完成字幕提取
        else:
            # 提取字幕
            file_name = f'Result/Subtitle/{aid}.srt'
            if not os.path.exists(file_name):
                pbar.update(1)
                continue
            res = read_srt(file_name)
            srt_result.append([aid,res])
            with open(f"Result/srt.csv", 'a+', newline='',encoding='utf-8') as file:
                writer = csv.writer(file)
                writer.writerows(srt_result)
            pbar.update(1)
    pbar.close()

    print('字幕提取完成')

def time_to_timestamp(time_str):
    # 分割时间字符串
    parts = time_str.split(':')
    hours = int(parts[0])
    minutes = int(parts[1])
    seconds_and_milliseconds = parts[2].split(',')
    seconds = int(seconds_and_milliseconds[0])
    milliseconds = int(seconds_and_milliseconds[1])
    
    # 计算总秒数
    total_seconds = hours * 3600 + minutes * 60 + seconds + milliseconds / 1000
    
    return total_seconds

def cal_speak_duration(srt):
    srt = eval(srt)
    start_time_total = 0
    end_time_total = 0
    speak_word = []
    for srt_sentence in srt:
        start_time_total += time_to_timestamp(srt_sentence['start_time'])
        end_time_total += time_to_timestamp(srt_sentence['end_time'])
        speak_word.append(srt_sentence['text'])
    return [end_time_total-start_time_total,speak_word]

def cal_word_count(text):
    word_count = 0
    if text == None:
        return 0
    else:
        for sentence in text:
            sentence = sentence.translate(str.maketrans('', '', string.punctuation))
            sentence = sentence.strip()
            word_count += len(sentence)
        return word_count

def process_srt(srt_df):
    srt_df[['speak_duration','speak_word']] = srt_df['srt'].apply(cal_speak_duration).apply(pd.Series)
    srt_df['word_count'] = srt_df['speak_word'].apply(cal_word_count)
    srt_df['speak_rate'] = srt_df['word_count']/srt_df['speak_duration']
    return srt_df

if __name__ == '__main__':

    file_name = f"List/aid_list.csv"
    aid_df = pd.read_csv(file_name,encoding='utf-8')
    
    get_srt(aid_df)
    srt_df = pd.read_csv(f"Result/srt.csv",encoding='utf-8')
    srt_df = process_srt(srt_df)
    srt_df[['aid','speak_duration','speak_word','word_count','speak_rate']].to_csv(f"Result/srt.csv",encoding='utf-8',index=False)