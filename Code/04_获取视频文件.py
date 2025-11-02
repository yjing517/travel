import subprocess
import time

from tqdm import tqdm
import pandas as pd
import os

session = "6d8d13fc%2C1742107963%2C630d6%89af599d%2C1744290621%2C2f856%2Aa1CjAyfXkrFFJWaREqdGyLtJysZ3PZHPeOvaGQ1EOtEEkJWVyg6SoV8prwR8pq-WMOHIoSVkNBMktTRmRYaXlDUS1IY2xLVHRrV25rVDhlejZqZHV0dGdkUXQ3NG1yZDRDeGp4cmVOSkJKa0hUZnhyN2RuSURFZEM3bUFtUTRZSWsyTGRxWjJod3B3IIEC"
def File_check(aid_df):

    print(f"{'*'*40}\t检查文件下载情况\t{'*'*40}")

    Video_file_list = []
    for filename in os.listdir("Result/Video_files/"):
        if filename.endswith(".mp4"):
            Video_file_list.append(int(os.path.splitext(filename)[0]))

    if set(aid_df['aid']).issubset(set(Video_file_list)):
        print("视频文件已全部爬取")
    else:
        print("视频文件未全部爬取")

    # Danmaku_ass_list = []
    # for filename in os.listdir("../Result/Danmaku/ass/"):
    #     if filename.endswith(".ass"):
    #         Danmaku_ass_list.append(int(os.path.splitext(filename)[0]))
    # if set(aid_df['aid']).issubset(set(Danmaku_ass_list)):
    #     print("弹幕(ass格式)已全部爬取")
    # else:
    #     print("弹幕(ass格式)未全部爬取")

    # Danmaku_xml_list = []
    # for filename in os.listdir("../Result/Danmaku/xml/"):
    #     if filename.endswith(".xml"):
    #         Danmaku_xml_list.append(int(os.path.splitext(filename)[0]))
    # if set(aid_df['aid']).issubset(set(Danmaku_xml_list)):
    #     print("弹幕(xml格式)已全部爬取")
    # else:
    #     print("弹幕(xml格式)未全部爬取")

def get_video_file(aid_df):

    print(f'开始下载视频文件、弹幕')
    pbar = tqdm(total=len(aid_df))

    for index, row in aid_df.iterrows():
        aid = int(row['aid'])
        title = row['title']
        # 已获取视频/弹幕/字幕文件
        # if os.path.exists(f"Result/Video_files/{aid}.mp4"):
        if os.path.exists(f"Result/Subtitle/{aid}.srt"):
        # if os.path.exists(f"Result/Danmaku/xml/{aid}.xml"):
            pbar.update(1)
        # 未获取视频文件
        
        else:
            commands = [
                # f"yutto -c \"{session}\" -d Result/Video_files/ --no-danmaku https://www.bilibili.com/video/av{aid}", # 视频文件
                f"yutto -c \"{session}\" -d Result/Danmaku/ass/ --danmaku-only https://www.bilibili.com/video/av{aid}", # 弹幕ass格式
                f"yutto -c \"{session}\" -d Result/Danmaku/xml/ --danmaku-only -df \"xml\" https://www.bilibili.com/video/av{aid}", # 弹幕xml格式
                f"yutto -c \"{session}\" -d Result/Subtitle/ --subtitle-only https://www.bilibili.com/video/av{row['aid']}", # 字幕
            ]
            for command in commands:
                try:
                    # 执行命令并获取输出结果
                    # if index>=23000:
                    result = subprocess.run(command, shell=True)
                    # print("输出结果为:\n", result)
                    old_filename = get_latest_downloaded_file(f"Result/Video_files/")
                    new_filename = f"Result/Video_files/{aid}.mp4"
                    os.rename(f"Result/Video_files/{old_filename}", new_filename)

                except Exception as e: 
                    print("命令执行失败！错误信息为:\n", e)
            
            old_filename = get_latest_downloaded_file(f"Result/Danmaku/ass/")
            new_filename = f"Result/Danmaku/ass/{aid}.ass"
            os.rename(f"Result/Danmaku/ass/{old_filename}", new_filename)
            
            old_filename = get_latest_downloaded_file(f"Result/Danmaku/xml/")
            new_filename = f"Result/Danmaku/xml/{aid}.xml"
            os.rename(f"Result/Danmaku/xml/{old_filename}", new_filename)

            pbar.update(1)
            # time.sleep(5)
    pbar.close()

    print('视频文件、弹幕下载完毕')

def get_latest_downloaded_file(directory):
  files = os.listdir(directory)
  files_with_mtime = [(os.path.getmtime(os.path.join(directory, f)), f) for f in files]
  files_with_mtime.sort(reverse=True)
  return files_with_mtime[0][1]

if __name__ == '__main__':
    aid_df = pd.read_csv(f"List/aid_list.csv",encoding='utf-8')
    get_video_file(aid_df)
    # File_check(aid_df)