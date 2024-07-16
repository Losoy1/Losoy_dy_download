import json
import os
import pandas as pd
from datetime import datetime
from dyspider import Search_Content

def dy_work_json_to_excel(work_info_json_path, result_dir, keyword):
    # 获取当前时间，用于创建文件名
    now = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    result_path = os.path.join(result_dir, f"{keyword}.xlsx")

    # 确保结果目录存在
    os.makedirs(result_dir, exist_ok=True)

    work_dir_list = os.listdir(work_info_json_path)
    for work_id in work_dir_list:
        print(f"处理作品： {work_id}")
        comment_list_file_path = f"{work_info_json_path}/{work_id}/comment_list.json"
        meta_data_file_path = f"{work_info_json_path}/{work_id}/metadata.json"

        comment_list = []
        metadata = {}

        # 检查元数据文件是否存在
        if not os.path.exists(meta_data_file_path):
            print(f"作品：{work_id} 的元数据文件不存在，跳过")
            continue

        with open(meta_data_file_path, "r", encoding='UTF-8') as mfile:
            meta_data_json_str = mfile.read()
            origin_metadata = json.loads(meta_data_json_str)
            author_info = origin_metadata["author_info"]
            metadata["作品id"] = origin_metadata["id"]
            metadata["作品链接"] = origin_metadata["url"]
            metadata["作品标题"] = origin_metadata["title"]
            metadata["作品点赞数"] = origin_metadata["favorite_num"]
            metadata["作品评论数"] = origin_metadata["comment_num"]
            metadata["作品发布时间"] = origin_metadata["release_time"]
            metadata["作者名字"] = author_info["name"]
            metadata["作者主页"] = author_info["main_page"]
            metadata["作者粉丝数"] = author_info["follower_num"]
            metadata["作者获赞数"] = author_info["praise_num"]

        # 检查评论列表文件是否存在
        if not os.path.exists(comment_list_file_path):
            print(f"作品：{work_id} 的评论列表文件不存在，跳过")
            continue

        with open(comment_list_file_path, "r", encoding='UTF-8') as cfile:
            comment_list_json_str = cfile.read()
            origin_comment_list = json.loads(comment_list_json_str)

        for origin_comment_info in origin_comment_list:
            comment_info = {}
            for key in metadata:
                comment_info[key] = metadata[key]
            comment_info["评论数据爬取时间"] = origin_comment_info.get("data_snapshot_time")
            comment_info["评论用户名"] = origin_comment_info.get("user_name")
            comment_info["评论用户主页"] = origin_comment_info.get("main_page")
            comment_info["评论时间和地点"] = origin_comment_info.get("comment_time_and_location")
            comment_info["评论内容"] = origin_comment_info.get("comment_text")
            comment_info["评论被赞数"] = origin_comment_info.get("praise_num")
            comment_list.append(comment_info)

        save_comment_info_to_excel(result_path, comment_list, work_id)

def save_comment_info_to_excel(result_path, comment_list, work_id):
    if len(comment_list) == 0:
        print(f"作品：{work_id}无评论，跳过")
        return

    # 检查文件是否存在，如果不存在则创建一个空的Excel文件
    if not os.path.exists(result_path):
        df = pd.DataFrame()
        with pd.ExcelWriter(result_path, engine='openpyxl') as writer:
            df.to_excel(writer)  # 创建一个空的Excel文件

    result = {}
    for key in comment_list[0]:
        result[key] = []

    for comment_info in comment_list:
        for key in result:
            result[key].append(comment_info.get(key, ""))

    df = pd.DataFrame(result)
    with pd.ExcelWriter(result_path, mode='a', engine='openpyxl') as writer:
        df.to_excel(writer, sheet_name=work_id)
        print(f"作品：{work_id}存储成功")

if __name__ == '__main__':
    dy_work_json_to_excel(os.path.dirname(__file__) + f'/spider/work/{Search_Content}', os.path.dirname(__file__) + r'/spider/result',Search_Content)


