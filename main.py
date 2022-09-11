'''
 @Author    Ray
 @Date      2022-07-25
 @Func      项目运行文件
 @Version   v1.0
 @Note      无
'''

from misstv.parser      import  get_url
from misstv.folder      import  get_folder
from misstv.basefile    import  get_base_file
from misstv.tsfile      import  get_ts_list
from misstv.crawler     import  get_video_file
from misstv.merger      import  merge_video_file
from misstv.deletefile  import  delete_base_file


def app():
    done_list = []      #已完成列表
    failed_list = []    #未完成列表

    ## 获取需要下载的url列表
    url_list = get_url()
    
    ## 循环列表下载影片
    while (len(url_list) != 0):
        url = url_list[-1]
        name = url.split('/')[-2]

        # 1.新建影片文件夹
        is_done, folder_path = get_folder(name)

        if not is_done:
            print("\n--------------------------------------------------------------------")
            print(f"-影片 {name} 开始下载, 剩余 {len(url_list)-1} 个待下载")

            # 2.获取m3u8文件和封面
            download_url, m3u8_path, exist = get_base_file(folder_path, url)
            
            if not exist:   #番号不存在
                url_list.pop()
                print(f" !ERROR: {name} 不存在或网站无资源")
                failed_list.append(name)
            elif len(download_url) == 0:    #链接失败
                print(f" !ERROR: {url} 连接失败, 稍后重试")
            else:
                # 3.根据m3u8文件获取ts列表
                ci, ts_list = get_ts_list(download_url, m3u8_path)

                # 4.爬取ts片段
                get_video_file(ci, folder_path, ts_list)

                # 5.合并ts片段
                merge_video_file(folder_path, ts_list)

                # 5.刪除过程性文件
                delete_base_file(folder_path)

                done_list.append(name)
                print(f"-影片 {name} 下载完成")
                url_list.pop()
        else:
            done_list.append(name)
            url_list.pop()
            
    ## 输出结束提示
    print("\n--------------------------------------------------------------------")
    print(f"-本次成功下载 {len(done_list)} 个影片, 共有 {len(failed_list)} 个不存在的番号")
    print("  -成功: ", end='')
    for i in done_list:
        print(i, end=' ')
    print("\n  -失败: ", end='')
    for i in failed_list:
        print(i, end=' ')
    print("")


if __name__=="__main__":
    app()
