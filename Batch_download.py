'''
每次批量下载前需要将爬取的url在Web端（127.0.0.1）进行解析，解析后才能下载，每次解析30个视频，每次下载只能下载一个种类的所有视频。
如果下载不成功请在Douyin_TikTok_Download_API/crawlers/douyin/web/config.yaml中更换Cookie（F12-网络-XHR-下滑抖音视频页面-get_conversation_list)
cmd 运行以下 重新部署
docker pull evil0ctal/douyin_tiktok_download_api:latest
docker run -d --name douyin_tiktok_api -p 80:80 evil0ctal/douyin_tiktok_download_api
'''
import requests
import json
import os
#请输入本次搜索的关键词，便于放入对应文件夹
Search_Content = "深圳联通客服不专业不解决问题"

video_url_list_path = f'D:\\ShiXi\\douyin_comment_spider\\spider\\search\\{Search_Content}\\video_url_list.json'
with open(video_url_list_path, 'r', encoding='utf-8') as file:
    urls = json.load(file)

# 确定视频保存的路径，并创建目录
save_path = f'D:\\ShiXi\\douyin_comment_spider\\spider\\search\\{Search_Content}\\video'
os.makedirs(save_path, exist_ok=True)

# 遍历URL列表，并下载每个视频
for url in urls:
    download_url = f"http://127.0.0.1/api/download?url={url}&prefix=true&with_watermark=false"
    response = requests.get(download_url)

    # 检查请求是否成功
    if response.status_code == 200:
        video_content = response.content
        video_name = url.split('/')[-1] + '.mp4'
        full_path = os.path.join(save_path, video_name)

        # 保存视频文件
        with open(full_path, 'wb') as video_file:
            video_file.write(video_content)
        print(f"Downloaded {video_name}")
    else:
        print(f"Failed to download video from {url}")
