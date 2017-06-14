import os

'''
-rw-r--r-- = 0644(octal) = 000 110 100 100(binary) = 420(decimal)
'''
_0644_ = 420
_0600_ = 384
_0755_ = 493
_0750_ = 488
_0777_ = 511

os.chmod('/media/xuananh/data/Temp/test.txt', _0777_)

os.chmod('aaa', _0777_)
