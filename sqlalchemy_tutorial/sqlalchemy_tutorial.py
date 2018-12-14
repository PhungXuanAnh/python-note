# -*- coding: utf-8 -*-

# các bước code được thực hiện theo link: https://docs.sqlalchemy.org/en/latest/orm/tutorial.html

from sqlalchemy.orm import sessionmaker
from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine
import sqlalchemy

print("======================= kiểm tra version")
print(sqlalchemy.__version__)

print("======================= kết nối database")
engine = create_engine('sqlite:///:memory:', echo=True)
# echo: là cờ để cài đặt/kích hoạt logging cho SQLAlchemy, nó dựa trên logging của python
# nếu bật nó thì sẽ nhìn thấy tất cả các câu lệnh SQL được tạo
# để tạo url kết nối đến các loại database khác như mysql, posgresql..
# tham khảo link: https://docs.sqlalchemy.org/en/latest/core/engines.html#database-urls

print("======================= khai báo một mapping (hay 1 class mô tả 1 bảng)")
# khi sử dụng ORM, tiến trình bắt đầu bằng cách mô tả các bảng dử liệu,
# sau đó là định nghĩa các class được ánh xạ đến các bảng trên.
# trong SQLAlchemy 2 việc trên được thực hiện cùng nhau sử dụng Declarative
# tạo ra một lớp cơ sở (Base). Ứng dụng thường chỉ có duy nhất một Base class
Base = declarative_base()
# bây giờ chúng ta sẽ định nghĩa các class mô tả bảng dữ liệu kế thừa từ Base class
# tham số 'bind' gắn Base vào kết nối đến cơ sở dữ liệu được khai báo ở trên
class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    name = Column(String)
    fullname = Column(String)
    password = Column(String)

    def __repr__(self):
        # hàm này trả về định dạng dễ đọc của đối tượng User
        return "<Users(name='{}', fullname='{}', password={})>".format(
            self.name, self.fullname, self.password
        )

print('----- User.__table__: ', User.__table__)
# Ngoài ra có thể tạo các hàm trợ giúp sử dụng minxin class:
# https://docs.sqlalchemy.org/en/latest/orm/extensions/declarative/mixins.html#declarative-mixins

print("======================= tạo Schema")
Base.metadata.create_all(engine)

print("======================= tạo một Instance của Mapped Class")
ed_user = User(name='ed',
               fullname='Ed Jones',
               password='edspassword')
print(ed_user.id)
print(ed_user.name)
print(ed_user.password)
# lưu ý là khai báo trên vẫn chưa được commit lên database server, vì vậy id sẽ là None

print("======================= tạo Session")
# chúng ta đã sẵn sàng nói chuyện với database, điều khiển quá trình này là Session
# khi cài đặt ứng dùng lần đầu, cùng chỗ gọi hàm create_engine(), chúng ta định
# nghĩa một class Session phục vụ như một nhà máy (factory) tạo mới các đối tượng Session
Session = sessionmaker(bind=engine)
# trong trường hợp chưa không muốn gắn engine luôn thì khai báo như sau:
Session1 = sessionmaker()
# khi nào nào tạo engine và kết nối đến nó sử dụng ham configure()
Session1.configure(bind=engine)
# xong, bây giờ, khi nào cần nói chuyện với database thì tạo 1 session
session = Session()
# session trên liên kết với engine nhưng chưa mở 1 kết nối nào, khi lần đầu
# kết sử dụng, nó sẽ lấy một kết nối từ một nhóm kết nối giữ bởi engine, và
# giữ kết nối này đến khi commit thay đổi hoặc đóng session object

print("======================= thêm và cập nhật đối tượng/bảng")
ed_user = User(name='ed',
               fullname='Ed Jones',
               password='edspassword')
session.add(ed_user)            
# lúc này đối tượng đang chờ, chưa có SQL nào được phát ra và đối tượng chưa được mô tả
# bởi một hàng nào trong database. Session sẽ phát ra SQL để duy trì Ed Jones ngay khi cần,
# sử dụng một tiến trình gọi là phun (flush). Nếu chúng ta truy vấn database để lấy Ed Jones,
# tất cả những thông tin đang chờ sẽ được phun ra và truy vấn được phát ra ngay lập tức sau đó.
# Ví dụ, bên dưới ta tạo 1 đối tượng truy vấn (Query) lạp vào đối tượng User, lọc theo name = ed,
# và chỉ lấy kết quả đầu tiên trong danh sách đầy đủ các của các hàng. Một đối tượng User
# được tra về tương đương với đối tượng ta đã tạo ở trên
our_user = session.query(User).filter_by(name='ed').first()
print('----- our_user = ', our_user)
# trong thực tế, Session đã nhận ra rằng hàng trả về tương tự một hàng được thể hiện trong bản đồ
# đối tượng bên trong của nó (its internal map of object), vì vậy chúng ta thực sự lấy lại đúng đối
# tượng mà chúng ta đã thêm vào ở trên:
print('----- ed_user is our_user = ', ed_user is our_user)
# Khái niệm ORM được biết như là một bản đồ nhận dạng và đảm bảo tất cả các hoạt động trên một
# hàng cụ thể trong Session hoạt động trên cùng một bộ dữ liệu. Khi một đối tượng với một primary key
# được biểu diễn trong Session, tất cả các truy vấn SQL trong Session đó luôn tra về cùng một 
# đối tượng Python cho primary key đó, sẽ có lỗi nếu cố gắn tạo một đối tượng thứ 2 cùng primary
# với một đối tượng đã tồn tại sẵn.
# Chúng ta có thể thêm nhiều đối tượng User trong một lệnh add_all()
session.add_all([
    User(name='wendy', fullname='Wendy Williams', password='foobar'),
    User(name='mary', fullname='Mary Contrary', password='xxg527'),
    User(name='fred', fullname='Fred Flinstone', password='blah')])
# ta đã tạo một password không quá bảo mật cho người dùng Ed, hãy thay đổi nó:
ed_user.password = 'f8s7ccs'
# Session đang để ý, nó biết Ed Jones đã bị thay đổi
print('----- session.dirty: ', session.dirty)
# và 3 đối tượng mới đang chờ:
print('----- session.new: ', session.new)
# bây giờ, ta yêu cầu Session phát ra tất cả các thay đổi đến database server và commit giao dịch
# được thực hiện từ đầu đến giờ. Để làm việc này dùng hàm commit(). Session phát ra biểu thức UPDATE
# để thay đổi password, và INSERT để thêm 3 đối tượng mới.
session.commit()
# connection resource được tham chiếu bởi session giờ trả lại cho connection pool, và sẽ lấy lại 
# mỗi khi cần
# bây giờ nếu xem id của Ed, nó sẽ không còn None nữa, mà có giá trị là:
print('----- ed_user.id: ', ed_user.id)
# sau khi Session  chèn hàng mới vào database, tất cả các định danh mới được tạo ra và bộ tạo database
# mặc định có sẵn trên các đối tượng, ngay lập tức hoặc qua lần truy cập đầu tiên. Trong trường hợp này
# toàn bộ các hàng được tải lại vì một phiên giao dịch mới bắt đầu sau khi chúng ta gọi commit().
# SQLAlchemy mặc định làm mới dữ liệu từ phiên giao dịch trước trong lần đầu truy cập trong một phiên
# giao dịch mới, vì vậy trạng thái gần nhất là có sẵn. Mức độ tải lại có thể được cấu hình như mô tả
# trong link: https://docs.sqlalchemy.org/en/latest/orm/session.html

# print("======================= khôi phục/quay lại ")
# Khi Session làm việc bên trong một phiên giao dịch, ta có thể khôi phục thay đổi đã làm. Hãy tạo 2 thay 
# đổi và khổi phục, tên của ed_users là Edwardo:
ed_user.name = 'Edwardo'
# và ta sẽ thêm một user lỗi khác, fake_user:
fake_user = User(name='fakeuser', fullname='Invalid', password='12345')
session.add(fake_user)
# truy vấn session, ta có thể thấy rằng nó đã được phun (flushed) vào phiên giao dịch hiện tại
print('----- ', session.query(User).filter(User.name.in_(['Edwardo', 'fakeuser'])).all())
# chạy khôi phục, ta có thể thấy rằng name của ed_used trở lại ed, và fake_user bị đã ra khỏi session
session.rollback()
print('----- ed_user.name: ', ed_user.name)
print('----- fake_user in session: ', fake_user in session)
# chạy lệnh SELECT để minh họa những thay đổi với database
print('----- ', session.query(User).filter(User.name.in_(['ed', 'fakeuser'])).all())

print("======================= truy vấn")
