'''
 @Author    Ray
 @Date      2022-07-25
 @Func      项目配置文件, 包含各种常量参数
 @Version   v1.0
 @Note      无
'''

# 视频页根url
video_base_url = 'https://missav.com/en/'

# 影片保存根文件夹(绝对路径或相对路径)
video_base_path = '.\\video'

# 429睡眠时间
sleep_time = 0.1

# 并行线程数
worker_num = 8

# 普通header
nor_headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.0.0 Safari/537.36',
}

# 爬取请求header
crawl_header = {
    'ccept-encoding': 'gzip, deflate, br',
    'accept-language': 'en-US,en;q=0.9,ja;q=0.8,zh-CN;q=0.7,zh;q=0.6',
    'origin': 'https://missav.com',
    'referer': 'https://missav.com/',
    'sec-ch-ua': '".Not/A)Brand";v="99", "Google Chrome";v="103", "Chromium";v="103"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'same-site',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.0.0 Safari/537.36'
}
