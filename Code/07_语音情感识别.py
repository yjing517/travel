import pandas as pd
import sys
from speechbrain.inference.diarization import Speech_Emotion_Diarization
sys.path.append("../..")
import os
import csv
from tqdm import tqdm

def audio2emo(aid_df,audio_emo_df):
    print(f'开始音频情感识别')
    pbar = tqdm(total=len(aid_df))

    from funasr import AutoModel
    model = AutoModel(model="iic/emotion2vec_base_finetuned")

    for index, row in aid_df.iterrows():
        audio2emo_result = []
        # 已完成语音情感识别
        if row['aid'] in audio_emo_df['aid'].values:
            pbar.update(1)
        # 未完成语音情感识别
        else:
            file_name = f"../Result/Audio/{row['aid']}.wav"
            res = model.generate(file_name, output_dir="./outputs", granularity="utterance", extract_embedding=False)
            audio2emo_result.append(
                [row['aid'], row['title'], res])

            with open(f"../Result/audio2emo.csv", 'a+', newline='') as file:
                writer = csv.writer(file)
                writer.writerows(audio2emo_result)

            pbar.update(1)
    pbar.close()

    print('音频情感识别完成')

def File_check(aid_df):

    print(f"{'*'*40}\t检查音频情感识别情况\t{'*'*40}")

    audio2text_df = pd.read_csv(f"../Result/audio2emo.csv")
    if set(aid_df['aid']).issubset(set(audio2text_df['aid'])):
        print("音频情感识别已全部完成")
    else:
        print("音频情感识别 未 全部完成")

    print(f"{'*' * 100}")

if __name__ == '__main__':

    aid_df = pd.read_csv(f"../List/aid_list.csv")

    if os.path.exists(f"../Result/audio2emo.csv"):
        audio_emo_df = pd.read_csv(f"../Result/audio2emo.csv")
    else:
        audio_emo_df = pd.DataFrame(columns=['title', 'aid', 'res'])
        audio_emo_df.to_csv(f"../Result/audio2emo.csv", index=False)


    audio2emo(aid_df,audio_emo_df)
    # File_check(aid_df)