'''
 @Author    Ray
 @Date      2022-07-25
 @Func      ts片段爬取
 @Version   v1.0
 @Note      无
'''

import os
import time
import copy
import requests
import concurrent.futures

from functools import partial
from misstv.config import crawl_header, sleep_time, worker_num


def scrape(ci, folder_path, download_list, urls):
    os.path.split(urls)
    fileName = urls.split('/')[-1][0:-3]
    saveName = os.path.join(folder_path, fileName + ".mp4")
    if os.path.exists(saveName):
        # 跳过已下载
        download_list.remove(urls)
    else:
        response = requests.get(urls, headers=crawl_header, timeout=100)
        if response.status_code == 200:
            content_ts = response.content
            if ci:
                content_ts = ci.decrypt(content_ts)  # 解碼
            with open(saveName, 'ab') as f:
                f.write(content_ts)
            download_list.remove(urls)
        elif response.status_code == 429:
            time.sleep(sleep_time)
        # 输出进度
        print('\r  -PROCESS: 正在下载 {0}, 剩余 {1} 个, status code: {2} \t'.format(
            urls.split('/')[-1], len(download_list), response.status_code), end='', flush=True)


def crawl(ci, folder_path, download_list):
    round = 0
    while(download_list != []):
        with concurrent.futures.ThreadPoolExecutor(max_workers=worker_num) as executor:
            executor.map(partial(scrape, ci, folder_path,
                                 download_list), download_list)
        round += 1
        print(f', round {round}')


def get_video_file(ci, folder_path, ts_list):
    download_list = copy.deepcopy(ts_list)
    start_time = time.time()
    print(' NOTICE: 开始下载 ' + str(len(download_list)) + ' 份文件, ', end='')
    print('预计等待时间 {0:.2f} 分钟(视影片长度和网络速度而定)'.format(len(download_list) / 120))

    crawl(ci, folder_path, download_list)   #开始爬取

    end_time = time.time()
    print(' NOTICE: 下载成功, 共计 {0:.2f} 分钟'.format((end_time - start_time) / 60))
