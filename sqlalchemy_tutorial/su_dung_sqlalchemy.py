import sqlalchemy
from models import User
from config import init_session


Session = init_session(server_type='mysql', server_echo=False)
# TODO: check again with postgres, it encountered error with password
# Session = init_session(server_type='postgres', server_echo=False)
session = Session()


def create_data():
    u1 = User('Phùng Xuân Anh', 'Văn Nhân - Phú Xuyên - Hà Nội')
    session.add(u1)
    session.commit()


def print_data():
    for user in session.query(User):
        print(type(user))
        print(user)
        print(user.name)
        print(user.address)


if __name__ == "__main__":
    print('SQLAlchemy version: {}'.format(sqlalchemy.__version__))
    # create_data()
    print_data()