import pandas as pd
import sys
sys.path.append("../..")
import os
import csv
from tqdm import tqdm
from scenedetect import detect, AdaptiveDetector,ContentDetector,ThresholdDetector
import cv2


def get_frame_by_scene(aid_df):
    print(f'开始提取视频帧(基于场景切换)')

    if os.path.exists(f"../Result/frame_scene.csv"):
        frame_scene_df = pd.read_csv(f"../Result/frame_scene.csv")
    else:
        frame_scene_df = pd.DataFrame(columns=['aid','scene','start_time','end_time','start_frame','end_frame'])
        frame_scene_df.to_csv(f"../Result/frame_scene.csv", index=False)

    pbar = tqdm(total=len(aid_df))

    for file_name in os.listdir('../Result/Frame/Frame_Scene'):
        print(file_name)

    for index, row in aid_df.iterrows():
        result = []
        # 已完成基于 场景切换 的视频帧提取
        if row['aid'] in frame_scene_df['aid']:
            pbar.update(1)
        # 未完成基于 场景切换 的视频帧提取
        else:
            file_path = f"../Result/Video_files/{row['aid']}.mp4"
            # scene_list = detect(file_path, ContentDetector(threshold=11))

            cap = cv2.VideoCapture(file_path)
            frame_count = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))

            # 一个视频最多20帧
            scene_list = detect(file_path, AdaptiveDetector(adaptive_threshold=2.2,min_scene_len=frame_count//20,window_width=4,min_content_val=3))

            for index, scene in enumerate(scene_list):
                frame_index = scene[0].get_frames()
                cap.set(cv2.CAP_PROP_POS_FRAMES, frame_index)
                ret, frame = cap.read()
                if ret:
                    cv2.imwrite(f"../Result/Frame/Frame_Scene/{row['aid']}_{index+1}.jpg", frame)
                else:
                    print(f"无法读取帧 {frame_index}。")
                result.append([row['aid'], index + 1,scene[0].get_timecode(), scene[0].get_frames(),scene[1].get_timecode(), scene[1].get_frames()])
            cap.release()

            with open(f"../Result/frame_scene.csv", 'a+', newline='') as file:
                writer = csv.writer(file)
                writer.writerows(result)
            pbar.update(1)
    pbar.close()
    print('提取视频帧完成(基于场景切换)')

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
    get_frame_by_scene(aid_df)
    # File_check(aid_df)