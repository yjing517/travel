import pandas as pd
import os
from Levenshtein import distance as levenshtein_distance

aid_df = pd.read_csv(f'./List/aid_list.csv',encoding='utf-8')
title_list = aid_df['title'].to_list()
aid_list = [str(aid) for aid in aid_df['aid'].to_list()]

def change_video_file_name(): 
    for file_name in os.listdir('./Result/Video_files'):
        if file_name.endswith('.mp4'):
            title = file_name.replace('.mp4','')
            if title in aid_list:
                continue
            file_type = '.mp4'
        elif file_name.endswith('_中文（自动生成）.srt'):
            title = file_name.replace('_中文（自动生成）.srt', '')
            if title in aid_list:
                continue
            file_type = '_中文（自动生成）.srt'
        elif file_name.endswith('_中文（中国）.srt'):
            title = file_name.replace('_中文（中国）.srt', '')
            if title in aid_list:
                continue
            file_type = '_中文（中国）.srt'
        elif file_name.endswith('_中文（自动翻译）.srt'):
            title = file_name.replace('_中文（自动翻译）.srt', '')
            if title in aid_list:
                continue
            file_type = '_中文（自动翻译）.srt'
        elif file_name.endswith('_英语（自动生成）.srt'):
            title = file_name.replace('_英语（自动生成）.srt', '')
            if title in aid_list:
                continue
            file_type = '_英语（自动生成）.srt'
        else:
            # print(file_name)
            continue
        if title in title_list:
            index = title_list.index(title)
            aid = aid_df.loc[index]['aid']
            try:
                os.rename(f'./Result/Video_files/{file_name}',
                        f'./Result/Video_files/{aid}{file_type}')
            except:
                # print(file_name)
                pass
        else:
            aid_df['distance'] = aid_df['title'].apply(lambda x: levenshtein_distance(title, x))
            closest_row = aid_df.loc[aid_df['distance'].idxmin()]
            aid = closest_row['aid']
            try:
                os.rename(f'./Result/Video_files/{file_name}',
                        f'./Result/Video_files/{aid}{file_type}')
            except:
                print(aid)
                print(file_name)

def change_srt_file_name():
    for file_name in os.listdir('./Result/Subtitle/'):
        if file_name.endswith('.srt'):
            title = file_name.replace('.srt','')
            if title in aid_list:
                continue
            else:
                title = ''.join(title.split('_')[:-1])
                if title in title_list:
                    index = title_list.index(title)
                    aid = aid_df.loc[index]['aid']
                    try:
                        os.rename(f'./Result/Subtitle/{file_name}',
                                f'./Result/Subtitle/{aid}.srt')
                    except:
                        if not file_name.endswith('_英语（自动生成）.srt'):
                            print(file_name)
                        pass
        # else:
        #     aid_df['distance'] = aid_df['title'].apply(lambda x: levenshtein_distance(title, x))
        #     closest_row = aid_df.loc[aid_df['distance'].idxmin()]
        #     aid = closest_row['aid']
        #     try:
        #         os.rename(f'./Result/Video_files/{file_name}',
        #                 f'./Result/Video_files/{aid}{file_type}')
        #     except:
        #         print(aid)
        #         print(file_name)

# change_video_file_name()
change_srt_file_name()