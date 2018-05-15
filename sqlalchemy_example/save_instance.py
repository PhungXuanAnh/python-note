# coding=utf-8
'''
Created on Apr 4, 2017

@author: xuananh
'''
from models import User, Session

# create instances of my user object
u1 = User('Phùng Xuân Anh')
u1.address = 'Văn Nhân - Phú Xuyên - Hà Nội'
# u1 = User('Phung Xuan Anh')
# u1.address = 'Van Nhan - Phu Xuyen - Ha Noi'
u1.profile = 'được đấy'

# u2 = User('Phùng Anh Hoa')
# u2.password = 'passwordOfHoa'
u2 = User('Phung Anh Hoa')
u2.password = 'passwordOfHoa'
u2.profile = 'được đó'

# testing
s = Session()
s.add_all([u1, u2])
s.commit()