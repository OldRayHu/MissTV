'''
 @Author    Ray
 @Date      2022-07-25
 @Func      合并ts片段文件
 @Version   v1.0
 @Note      无
'''

import os
import time


def merge_video_file(folder_path, ts_list):
    start_time = time.time()
    print(' NOTICE: 开始合成影片, ', end='')
    print('预计等待时间 {0:.2f} 秒(视影片长度和电脑性能而定)'.format(len(ts_list) / 65))

    err = False
    for i in range(len(ts_list)):
        file = ts_list[i].split('/')[-1][0:-3] + '.mp4'
        full_path = os.path.join(folder_path, file)
        video_name = folder_path.split(os.path.sep)[-1]
        if os.path.exists(full_path):
            with open(full_path, 'rb') as f1:
                with open(os.path.join(folder_path, video_name + '.mp4'), 'ab') as f2:
                    f2.write(f1.read())
        else:
            err = True
            break
    
    if err:
        print(" !ERROR: 合成 " + file + " 失败")
    else:
        end_time = time.time()
        print(' NOTICE: 合成成功, 共计 {0:.2f} 秒'.format(end_time - start_time))
