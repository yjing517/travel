import pandas as pd
import sys
sys.path.append("../..")
import os
import ffmpeg
from tqdm import tqdm

def get_audio(aid_df):
    print(f'开始切分音频')
    pbar = tqdm(total=len(aid_df))

    for index, row in aid_df.iterrows():
        aid = int(row['aid'])
        # print(aid)
        # 已获取音频文件
        if os.path.exists(f"Result/Audio/{aid}.mp3"):
            pbar.update(1)
        # 未获取音频文件
        else:
            vidoe_file = f"Result/Video_files/{aid}.mp4"
            if os.path.exists(vidoe_file):
                try:
                    ffmpeg.input(vidoe_file).audio.output(f"Result/Audio/{aid}.mp3").run(quiet=True,)
                except:
                    print(1)
            pbar.update(1)
    pbar.close()
    print('音频文件获取完毕')

def File_check(aid_df):

    print(f"{'*'*40}\t检查文件下载情况\t{'*'*40}")

    file_list = []
    for filename in os.listdir("Result/Audio/"):
        if filename.endswith(".mp3"):
            file_list.append(int(os.path.splitext(filename)[0]))
    if set(aid_df['aid']).issubset(set(file_list)):
        print("音频文件已全部获取")
    else:
        print("音频文件 未 全部获取")

    print(f"{'*' * 100}")


if __name__ == '__main__':
    aid_df = pd.read_csv(f"List/aid_list.csv")

    get_audio(aid_df)
    # File_check(aid_df)
