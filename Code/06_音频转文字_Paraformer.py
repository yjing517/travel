import pandas as pd
import sys
sys.path.append("../..")
from tqdm import tqdm
import os
import csv
import re
# from pydub import AudioSegment
from funasr import AutoModel
import torch

def audio2text(aid_df,audio2text_df):

    print(f'开始音频转文字')
    pbar = tqdm(total=len(aid_df))

    model_asr = AutoModel(
        model="iic/SenseVoiceSmall",
        trust_remote_code=True,
        vad_model="fsmn-vad",
        vad_kwargs={"max_single_segment_time": 30000},
        device="cuda:0",
    )
    model_vad= AutoModel(model="fsmn-vad",device="cuda:0")

    for index, row in aid_df.iterrows():
        ASR_result = []
        aid = int(row['aid'])
        # 已完成音频转文字
        if aid in audio2text_df['aid'].values:
            pbar.update(1)
        # 未完成音频转文字
        else:
            file_name = f"./Audio/{aid}.mp3"
            print(file_name)
            try:
                res_asr = model_asr.generate(input=file_name)
                res_vad = model_vad.generate(input=file_name)
                ASR_result.append(
                    [row['aid'], row['title'], res_asr[0]['text'],res_vad[0]['value']])
                with open(f"./Result/audio2text.csv", 'a+', newline='',encoding='utf-8') as file:
                    writer = csv.writer(file)
                    writer.writerows(ASR_result)
            except:
                pass

            pbar.update(1)
    pbar.close()

    print('音频转文字完毕')

def text_process():
    for index, row in pd.read_csv(f"./Result/audio2text.csv").iterrows():
        timestamp_left1 = 0
        timestamp_right1 = 0
        for index, word_timestamp in enumerate(eval(row['timestamp'])):
            timestamp_left1 += word_timestamp[0]
            timestamp_right1 += word_timestamp[1]

        timestamp_left2 = 0
        timestamp_right2 = 0
        for index, sentence_timestamp in enumerate(eval(row['res_vad'])):
            timestamp_left2 += sentence_timestamp[0]
            timestamp_right2 += sentence_timestamp[1]

        print(f"speak_duration_1 = {(timestamp_right1-timestamp_left1)/1000}s")
        print(f"speak_duration_2 = {(timestamp_right2-timestamp_left2)/1000}s")

        # exit()

def File_check(aid_df):

    print(f"{'*'*40}\t检查音频转文字情况\t{'*'*40}")

    audio2text_df = pd.read_csv(f"../Result/audio2text.csv",encoding='utf-8')
    if set(aid_df['aid']).issubset(set(audio2text_df['aid'])):
        print(f"音频转文字已全部完成,共{len(set(aid_df['aid']))}条")
    else:
        print(f"音频转文字 未 全部完成,视频共{len(set(aid_df['aid']))}条,完成音频转文字{len(set(audio2text_df['aid']))}条")

    print(f"{'*' * 100}")

def cut_wav(input_file,start_time,end_time,output_file):
    sound = AudioSegment.from_file(input_file, format="wav")
    cropped_sound = sound[start_time:end_time]
    cropped_sound.export(output_file, format="wav")

if __name__ == '__main__':
    # file_name = f"../List/aid_list.csv"
    file_name = f"./List/aid_list_new.csv"
    aid_df = pd.read_csv(file_name,encoding='utf-8')

    if os.path.exists(f"./Result/audio2text.csv"):
        audio2text_df = pd.read_csv(f"./Result/audio2text.csv",encoding='utf-8')
    else:
        col_list = ['aid','title','res_asr','res_vad']
        audio2text_df = pd.DataFrame(columns=col_list)
        with open(f"./Result/audio2text.csv", 'w+', newline='',encoding='utf-8') as file:
            writer = csv.writer(file)
            writer.writerow(col_list)

    audio2text(aid_df,audio2text_df)
    # File_check(aid_df)
    # cut_wav(f"../Result/Audio/1906329992.wav", 5060, 35980, f"../Result/Audio/new2.wav")
