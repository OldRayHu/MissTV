'''
 @Author    Ray
 @Date      2022-07-25
 @Func      创建影片文件夹
 @Version   v1.0
 @Note      无
'''

import os
from misstv.config import video_base_path


def get_folder(dirName):
    is_done = False
    folder_path = os.path.join(video_base_path, dirName)

    if not os.path.exists(folder_path):
        os.makedirs(folder_path)
    elif os.path.exists(folder_path+'\\'+dirName+'.mp4'):
        is_done = True

    return is_done, folder_path
