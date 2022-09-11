'''
 @Author    Ray
 @Date      2022-07-25
 @Func      删除过程性文件
 @Version   v1.0
 @Note      无
'''

import os


def delete_mp4(folder_path):
    files = os.listdir(folder_path)
    ori_mp4 = folder_path.split(os.path.sep)[-1] + '.mp4'
    ori_jpg = folder_path.split(os.path.sep)[-1] + '.jpg'
    for file in files:
        if file != ori_mp4 and file != ori_jpg:
            os.remove(os.path.join(folder_path, file))


def delete_m3u8(folder_path):
    files = os.listdir(folder_path)
    for file in files:
        if file.endswith('.m3u8'):
            os.remove(os.path.join(folder_path, file))


def delete_base_file(folder_path):
    # 删除m3u8文件
    delete_m3u8(folder_path)

    # 删除子mp4文件
    delete_mp4(folder_path)
    