import string
import random
import sqlalchemy
from models import User, Base
from config import init_session


Session, engine = init_session(server_type='postgres', server_echo=False)
# Session = init_session(server_type='mysql', server_echo=False)
session = Session()


def clean_database():
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    return True


def create_data():
    # u1 = User('Anh', 10, 'Ha Noi')
    # u2 = User('Binh', 21, 'Thai Binh')
    # u3 = User('Cuong', 100, 'Nam Dinh')
    # session.add_all([u1, u2, u3])

    for _ in range(0, 100):
        name = random.choice(['Anh', 'Binh', 'Cuong', 'Thang', 'Nghia', 'Hieu', 'Trang'])
        age = random.choice(range(0, 100))
        address = random.choice(["Ha Noi", "HCM", "Hue", "Da Nang", "Hai Phong", "Nam Dinh"])
        session.add(User(name, age, address))

    session.commit()


def query_data():
    for user in session.query(User):
        print('---------------')
        print(type(user))
        print(user)
        print(user.name)
        print(user.address)


def query_data_by_1_column():
    # kết quả trả về của query luôn là 1 tuple
    # để lấy kết quả của từng cột, dùng hàm query_data_by_2_column() bên dưới
    for name in session.query(User.name):
        print('---------------')
        print(name)


def query_data_by_2_column():
    for name, address in session.query(User.name, User.address):
        print('---------------')
        print(name)
        print(address)
        print(name, address)


def query_data_by_class_and_column():
    for row in session.query(User, User.name).all():
        print(row.User)
        print(row.name)


def query_filter_by():
    for user in session.query(User.name).filter_by(name='Anh'):
        print(user)


def query_filter():
    # NOTE: filter linh hoạt hơn filter_by, nó có thể dùng các toán tử Python

    print('--------------- == Anh')
    for user in session.query(User.name).filter(User.name == 'Anh'):
        print(user)

    print('--------------- != Anh')
    for user in session.query(User.name).filter(User.name != 'Anh'):
        print(user)

    print('--------------- like %Anh% , không phân biệt chữ hoa thường')
    for user in session.query(User.name).filter(User.name.like('%Anh%')):
        print(user)

    print('--------------- ilike %AnH% , phân biệt chữ hoa thường')
    for user in session.query(User.name).filter(User.name.ilike('%AnH%')):
        print(user)

    print("--------------- in_ ['Anh', 'Binh', 'Thao', 'Hoa']")
    for user in session.query(User.name).filter(User.name.in_(['Anh', 'Binh', 'Thao', 'Hoa'])):
        print(user)

    print("--------------- is null , có 2 cách")
    for user in session.query(User.name).filter(User.name.is_(None)):
        print(user)
    for user in session.query(User.name).filter(User.name == None):
        print(user)

    print("--------------- is not null, có 2 cách")
    for user in session.query(User).filter(User.name != None):
        print(user)
    for user in session.query(User).filter(User.name.isnot(None)):
        print(user)

    print("--------------- and, có 3 cách")
    # sử dụng and_()
    from sqlalchemy import and_
    for user in session.query(User).filter(and_(User.name == 'Anh', User.address == 'Ha Noi')):
        print(user)
    # hoặc gửi nhiều biểu thức đến filter()
    for user in session.query(User).filter(User.name == 'Anh', User.address == 'Ha Noi'):
        print(user)
    # hoặc xâu chuỗi nhiều cuộc gọi filter()/filter_by()
    for user in session.query(User).filter(User.name == 'Anh').filter(User.address == 'Ha Noi'):
        print(user)

    print("--------------- or")
    from sqlalchemy import or_
    for user in session.query(User).filter(or_(User.name == 'Anh', User.name == 'Binh')):
        print(user)

    print("--------------- match, chỉ có trong 1 vài db, vì thế có thể báo lỗi, vd dùng sqlite")
    try:
        for user in session.query(User).filter(User.name.match('Anh')):
            print(user)
    except Exception as e:
        print(e)


def query_order_offset_limit():
    for user in session.query(User).order_by(User.age).offset(15).limit(20):
        print(user)
    print('-----------------------------------------------------------------------')
    for user in session.query(User).filter(User.age.between(20, 50)).order_by(User.age).offset(15).limit(20):
        print(user)


def query_1_or_many_result():
    query = session.query(User).filter(User.name.like('%h%')).order_by(User.id)
    print('all():   ', query.all())
    print('first(): ', query.first())

    try:
        query.one()
    except Exception as e:
        # lấy đầy đủ tất cả các hàng,
        # nếu có nhiều hơn 1 hàng thì bị lỗi
        # vd trường hợp này bị lỗi
        print('one() lỗi:', e)
        pass
    print('one() k lỗi:   ', query.filter(User.id == 1).one())

    try:
        query.scalar()
    except Exception as e:
        # gọi one()
        # thành công thì trả về cột đầu tiên
        print('scalar() lỗi', e)
        pass
    print('scalar() k lỗi:   ', query.filter(User.id == 1).scalar())


if __name__ == "__main__":
    print('SQLAlchemy version: {}'.format(sqlalchemy.__version__))
    clean_database()
    create_data()
    # query_data_by_1_column()
    # query_data_by_2_column()
    # query_data_by_class_and_column()
    # query_filter_by()
    query_filter()
    query_order_offset_limit()
    # query_1_or_many_result()
