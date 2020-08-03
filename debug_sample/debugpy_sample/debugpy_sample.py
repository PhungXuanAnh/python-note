# -*- coding: utf-8 -*-
'''
Hướng dẫn:
    0. them debugpy vao requirements.txt của remote server và máy local
    1. thay địa chỉ remote server của dòng comment bên dưới
        đảm bảo vscode có thể kết nối đến remote server,
        ví dụ trong docker phải expose cổng, hoặc mở firewall
    2. thay đổi [host, port, localRoot, remoteRoot] trong file .vscode/launch.json
    3. chọn breakpoint, có 2 cách:
        3.1. Cách 1: chọn breakpoint trực tiếp bằng cái chấm màu đỏ,
            - khuyến khích dùng cách này,
            - LƯU Ý: breakpoint trên dòng bị comment hoặc dòng trắng không có tác dụng 
        3.2. Cách 2: dùng debugpy.breakpoint() như bên dưới 
    4. chạy file này
    5. vào mục Run của vscode, chọn `Python: Remote Attach`
    6. Click Run button 
'''
import time
import multiprocessing


def worker():
    print("====================== worker")
    
    import debugpy
    # debugpy.listen(("0.0.0.0", 5678))
    debugpy.listen(5678)
    debugpy.wait_for_client()
    # debugpy.breakpoint()

    i = 0
    while i < 10:
        print(i)
        i = i + 1


if __name__ == '__main__':
    p1 = multiprocessing.Process(target=worker)
    p1.start()

    a = "aaa-"
    b = "bbb-"
    c = "ccc"
    final = a + b + c
    print(final)
    