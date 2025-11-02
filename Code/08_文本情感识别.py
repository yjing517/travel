import pandas as pd
import sys
sys.path.append("../..")
import os
import csv
from tqdm import tqdm
from modelscope.pipelines import pipeline
from modelscope.utils.constant import Tasks

def audio2emo_title(aid_df):
    print(f'开始文本情感识别_title')

    if os.path.exists(f"../Result/text2emo_title.csv"):
        text2emo_title_df = pd.read_csv(f"../Result/text2emo_title.csv")
    else:
        text2emo_title_df = pd.DataFrame(columns=['aid','title_emo_binary','title_emo_multy'])
        text2emo_title_df.to_csv(f"../Result/text2emo_title.csv", index=False)

    pbar = tqdm(total=len(aid_df))
    # 二分类文本情感识别模型
    model_binary = pipeline(Tasks.text_classification, 'damo/nlp_structbert_sentiment-classification_chinese-base')
    # 多分类模型
    model_multy = pipeline(Tasks.text_classification, 'damo/nlp_structbert_emotion-classification_chinese-tiny',
                     model_revision='v1.0.0')
    for index, row in aid_df.iterrows():
        audio2emo_result = []
        # 已完成文本情感识别
        if row['aid'] in text2emo_title_df['aid'].values:
            pass
        # 未完成文本情感识别
        else:
            # 识别标题文本情感
            title = row['title']
            title_res_binary = model_binary(input=title)
            title_res_multy = model_multy(input=title)
            audio2emo_result.append([row['aid'],title_res_binary,title_res_multy])
            with open(f"../Result/text2emo_title.csv", 'a+', newline='') as file:
                writer = csv.writer(file)
                writer.writerows(audio2emo_result)

        pbar.update(1)
    pbar.close()

    print('文本情感识别完成_title')

def audio2emo_text(aid_df):
    print(f'开始文本情感识别_text')

    audio2text_df = pd.read_csv(f"../Result/audio2text.csv")
    if os.path.exists(f"../Result/text2emo_text.csv"):
        text2emo_text_df = pd.read_csv(f"../Result/text2emo_text.csv")
    else:
        text2emo_text_df = pd.DataFrame(columns=['aid','text_emo_binary','text_emo_multy'])
        text2emo_text_df.to_csv(f"../Result/text2emo_text.csv", index=False)


    pbar = tqdm(total=len(audio2text_df))
    # 二分类文本情感识别模型
    model_binary = pipeline(Tasks.text_classification, 'damo/nlp_structbert_sentiment-classification_chinese-base')
    # 多分类模型
    model_multy = pipeline(Tasks.text_classification, 'damo/nlp_structbert_emotion-classification_chinese-tiny',
                           model_revision='v1.0.0')
    for index, row in audio2text_df.iterrows():
        audio2emo_result = []
        # 已获完成文本情感识别
        if row['aid'] in text2emo_text_df['aid'].values:
            pbar.update(1)
        # 未完成文本情感识别
        else:
            # 识别文本情感
            text = row['text']
            text_res_binary = model_binary(input=text)
            text_res_multy = model_multy(input=text)
            audio2emo_result.append([row['aid'], text_res_binary, text_res_multy])
        with open(f"../Result/text2emo_text.csv", 'a+', newline='') as file:
            writer = csv.writer(file)
            writer.writerows(audio2emo_result)
        pbar.update(1)
    pbar.close()

    print('文本情感识别完成_text')

def File_check(aid_df):

    print(f"{'*'*40}\t检查文本情感识别情况\t{'*'*40}")

    audio2text_df = pd.read_csv(f"../Result/audio2emo.csv")
    if set(aid_df['aid']).issubset(set(audio2text_df['aid'])):
        print("文本情感识别已全部完成")
    else:
        print("文本情感识别 未 全部完成")

    print(f"{'*' * 100}")

if __name__ == '__main__':

    # file_name = f"../List/aid_list.csv"
    file_name = f"../List/aid_list_new.csv"
    aid_df = pd.read_csv(file_name)

    audio2emo_title(aid_df)
    # audio2emo_text(aid_df)

    # File_check(aid_df)