'''
 @Author    Ray
 @Date      2022-07-25
 @Func      获取ts文件url列表
 @Version   v1.0
 @Note      无
'''

import m3u8
import requests
from Crypto.Cipher import AES
from misstv.config import crawl_header


def get_ts_list(download_url,m3u8_path):
    # 1.读取m3u8的URI和IV
    m3u8_obj = m3u8.load(m3u8_path)
    m3u8_uri = ''
    m3u8_iv = ''
    for key in m3u8_obj.keys:
        if key:
            m3u8_uri = key.uri
            m3u8_iv = key.iv

    # 2.保存ts网址
    ts_list = []
    for seg in m3u8_obj.segments:
        ts_url = download_url + '/' + seg.uri
        ts_list.append(ts_url)

    # 3.有加密
    if m3u8_uri:
        m3u8_keyurl = download_url + '/' + m3u8_uri #key的网址
        # 读取key的內容
        response = requests.get(m3u8_keyurl, headers=crawl_header, timeout=100)
        contentKey = response.content
        vt = m3u8_iv.replace("0x", "")[:16].encode()    # IV取前16位
        ci = AES.new(contentKey, AES.MODE_CBC, vt)      # 构建解码器
    else:
        ci = ''

    return ci, ts_list
