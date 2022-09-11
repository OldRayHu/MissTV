'''
 @Author    Ray
 @Date      2022-07-25
 @Func      解析器, 命令行获取url
 @Version   v1.0
 @Note      无
'''

import argparse
from misstv.config import video_base_url


def init_parser():
    parser = argparse.ArgumentParser(description="MissAV Downloader")
    parser.add_argument('-f','--file', type=bool, default=False,
        help="Enter True to download according to file's contant")
    parser.add_argument('-u','--url', type=str, default="",
        help="MissAV URLs to download, divided by \',\'")
    parser.add_argument('-n','--name', type=str, default="",
        help="MissAV names to download, divided by \',\'")
    return parser


def get_url():
    parser = init_parser()
    args = parser.parse_args()
    
    url_list = []
    input_str = ""
    if (len(args.url)==0) and (len(args.name)==0) and (args.file is False):
        input_str = input('-输入单个MissAV网址:')
        url_list.append(input_str)
    elif (len(args.url)!=0):
        input_str = args.url
        url_list = input_str.split(',')
    elif (len(args.name)!=0):
        input_str = args.name
        input_list = input_str.split(',')
        for i in input_list:
            url_list.append(video_base_url+i.lower()+'/')
    elif (args.file is True):
        file = open('download.txt','r')
        for line in file:
            line = line.replace("\n","")
            url_list.append(video_base_url+line.lower()+'/')
    
    return url_list
    