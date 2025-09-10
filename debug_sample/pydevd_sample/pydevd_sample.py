# -*- coding: utf-8 -*-
'''
Hướng dẫn debug:
    - Chọn break point bằng cách duple click lên số dòng bên trái editor
    khi hiện lên dấu màu xanh là được
    - Sau đó chọn Run -> Debug hoặc nhấn F11
    - Các phím tắt để chạy debug:
        F5: Step into, nhảy vào hàm đang chạy
        F6: Step over, thực hiện dòng hiện tại và nhảy qua dòng tiếp theo
        F7: Step return, thực hiện hàm hiện và return luôn

        Ctrl+F2: Terminal, dừng debug server

Hướng dẫn remote debug hoặc debug multiprocess
    - cài đặt trên máy local và remote server: pip install pydevd
    - đặt hàm pydevd.settrace() tại vị trí muốn làm break-point
    - chỉnh sửa các tham số trong hàm pydevd.settrace(): 
        + host: là ip của debug server - máy tính chạy eclipse, mặc định là local
        + port: là port của debug server, mặc định là 5678
    - copy nội dung file này lên remote server
    - start debug server trên eclipse:
        + Chuyển sang Debug perspective, chọn Pydev -> Start Debug Server
    - chạy file python này trên remote server
    - theo dõi trên giao diện eclipse, chạy các phím tắt debug như bình thường

################## VERY IMPORTANCE ###################
NOTE 1: khi debug flask với multiproces,
        phải cài đặt rõ ràng tham số thread là False như sau:
             app.run(debug=False, thread=False)
        để chắc chắn có thể kết nối đến remote server
      
NOTE 2: các bước test khi không thể kết nối đến remote server
        1. debug file này với break-point
        2. debug file này với pydevd.settrace() trên máy local
        3. telnet đến remote server
        4. debug file này với pydevd.settrace() và remote server
'''


import multiprocessing


def worker():
    import pydevd
    pydevd.settrace(host="localhost",
                    port=5678,
                    stdoutToServer=True,
                    stderrToServer=True,
                    suspend=False  # Don't block if debugger not attached
                    )
#     import pydevd;pydevd.settrace()
    var1 = 4
    while var1 < 9:
        var1 = var1 + 1
        print(var1)


if __name__ == '__main__':
    # khong duoc thi chay thu dong duoi
    # /home/ubuntu/.validium-env/lib/python2.7/site-packages/pydevd_file_utils.py
    # /usr/local/lib/python2.7/dist-packages/pydevd_file_utils.py
    # PATHS_FROM_ECLIPSE_TO_PYTHON='''[["path to local source","path to remote source"]]'''
    # export PATHS_FROM_ECLIPSE_TO_PYTHON='''[["/media/xuananh/data/Dropbox/Viosoft/Eclipse_workspace/validium-nsb-backend1","/home/ubuntu/Dropbox/validium-nsb-backend1"]]'''
    p1 = multiprocessing.Process(target=worker, args=())
    p1.start()

    var1 = 0
    while var1 < 3:
        var1 = var1 + 1
        print(var1)
