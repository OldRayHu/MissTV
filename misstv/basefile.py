'''
 @Author    Ray
 @Date      2022-07-25
 @Func      获取m3u8文件和封面
 @Version   v1.0
 @Note      无
'''

import re
import os
import m3u8
import shutil
import requests

from bs4 import BeautifulSoup
from misstv.config import nor_headers, crawl_header


## js eval()加密解密器
def decode_js_packed_codes(code):
    def encode_base_n(num, n, table=None):
        FULL_TABLE = '0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ'
        if not table:
            table = FULL_TABLE[:n]
 
        if n > len(table):
            raise ValueError('base %d exceeds table length %d' % (n, len(table)))
 
        if num == 0:
            return table[0]
 
        ret = ''
        while num:
            ret = table[num % n] + ret
            num = num // n
        return ret
 
    pattern = r"}\('(.+)',(\d+),(\d+),'([^']+)'\.split\('\|'\)"
    mobj = re.search(pattern, code)
    obfucasted_code, base, count, symbols = mobj.groups()
    base = int(base)
    count = int(count)
    symbols = symbols.split('|')
    symbol_table = {}
 
    while count:
        count -= 1
        base_n_count = encode_base_n(count, base)
        symbol_table[base_n_count] = symbols[count] or base_n_count
 
    return re.sub(
        r'\b(\w+)\b', lambda mobj: symbol_table[mobj.group(0)],
        obfucasted_code)


def get_base_file(folder_path, url):
    # 0.获取网页源代码
    try:    #尝试连接网站
        response = requests.get(url, headers=nor_headers, timeout=10)
    except: #连接失败,返回空地址,稍后重试
        return "","",True
    if response.status_code == 404: # 番号不存在
        shutil.rmtree(folder_path)
        return "","",False
    r_text = response.text
    soup = BeautifulSoup(r_text,"html.parser")

    # 1.对js加密代码解密
    encode_start = r_text.find('eval(')
    encode_end = r_text.find(')\n',encode_start)
    encode_code = r_text[encode_start: encode_end+1]
    encode_code = encode_code.replace("\\\\","\\").replace("\\'","\'")
    decode_code = decode_js_packed_codes(encode_code)

    # 2.根据解密代码获得原始sourse url
    playlist_start = decode_code.find('http')
    playlist_url = decode_code[playlist_start:-1]
    download_url = '/'.join(playlist_url.split('/')[:-1])

    # 3.下载原始playlist.m3u8
    try:
        playlist_r = requests.get(playlist_url, headers=crawl_header, timeout=100)
    except:
        return "","",True
    playlist_path = os.path.join(folder_path, 'playlist.m3u8')
    playlist_fh = open(playlist_path, "wb")
    playlist_fh.write(playlist_r.content)
    playlist_fh.close()

    # 4.构造影片对应的video.m3u8地址
    playlist_obj = m3u8.load(playlist_path)
    m3u8_url_suffix = '1280x720/video.m3u8'
    if len(playlist_obj.data['playlists'])!=0:
        m3u8_url_suffix = playlist_obj.data['playlists'][0]['uri']
    m3u8_url = download_url + '/' + m3u8_url_suffix
    try:
        m3u8_r = requests.get(m3u8_url, headers=crawl_header, timeout=100)
    except:
        return "","",True
    print(' NOTICE: JS解密成功, 成功下载 m3u8 文件')
    m3u8_path = os.path.join(folder_path, '.m3u8')
    m3u8_fh = open(m3u8_path, "wb")
    m3u8_fh.write(m3u8_r.content)
    m3u8_fh.close()

    # 5.修改ts文件下载的基url
    download_url = '/'.join(m3u8_url.split('/')[:-1])

    # 6.保存封面
    cover_name = f"{os.path.basename(folder_path)}.jpg"
    cover_path = os.path.join(folder_path, cover_name)
    if os.path.exists(cover_path):
        return download_url, m3u8_path, True
    for meta in soup.find_all("meta"):
        cover_url = meta.get("content")
        if not cover_url:
            continue
        elif "cover.jpg" in cover_url:
            try:
                cover_r = requests.get(cover_url)
                cover_fh = open(cover_path, "wb")
                cover_fh.write(cover_r.content)
                print(f" NOTICE: 封面下载完成, 文件名为 {cover_name}")            
            except Exception as e:
                print(f" !ERROR: 封面下载失败, 报错为 {e}")
            break

    return download_url, m3u8_path, True
