'''
NOTE 1: 
    1. ptvsd khong giong nhu pydevd, phai dat breakpoint thi debugger moi dung
    2. tot nhat dat breakpoint tai nhieu diem truoc diem muon dung cho chac
        khong hieu sao ma no khong dung 
    3. Run file
    4. Start bugging

    Vi du: muon debug tai dong 23 thi tot nhat dat breakpoint
            tai cac dong  22, 23, 24 hoac nhieu hon cho chac,
            no se dung o dong 23 hoac 24
NOTE 2:
    1. Khi debug multi process hoac remote debug thi an cac buoc cham thoi
        khong co debugger no khong tra ve kip ket qua


launch.json tren may 10.76.241.113:  {
            "name": "Python: Attach",
            "type": "python",
            "request": "attach",
            "localRoot": "${workspaceFolder}/debug_sample/ptvsd_sample",
            "remoteRoot": "/root/",
            "port": 12345,
            "secret": "my_secret",
            "host": "10.76.241.113"  --> ip cua may remote
        },
launch.json tren may localhost:  {
            "name": "Python: Attach",
            "type": "python",
            "request": "attach",
            "localRoot": "${workspaceFolder}/debug_sample/ptvsd_sample",
            "remoteRoot": "${workspaceFolder}/debug_sample/ptvsd_sample",
            "port": 12345,
            "secret": "my_secret",
            "host": "localhost"  --> ip cua may
        },        
'''
import multiprocessing


def worker():
    import ptvsd
    ptvsd.enable_attach("my_secret", address=('localhost', 3000))
    ptvsd.wait_for_attach()

    var1 = 4
    while var1 < 9:
        print(var1)
        var1 = var1 + 1


if __name__ == '__main__':
    p1 = multiprocessing.Process(target=worker, args=())
    p1.start()

    # import ptvsd
    # ptvsd.enable_attach("my_secret", address = ('0.0.0.0', 12345))
    # ptvsd.wait_for_attach()

    var1 = 0
    while var1 < 3:
        var1 = var1 + 1
        print(var1)
