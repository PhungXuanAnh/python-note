from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker


USER = 'root'
PASSWORD = '12345'
HOST = 'localhost'

MYSQL_PORT = 4321
POSTGRES_PORT = 1234

DB = 'my_test_db'

CHARSET = 'utf8'  # NOTE: it import to automatically convert(encode/decode) data to unicode using utf8
MYSQL_URL = 'mysql+pymysql://{user}:{password}@{host}:{port}/{database}?charset={charset}'\
    .format(user=USER,
            password=PASSWORD,
            host=HOST,
            port=MYSQL_PORT,
            database=DB,
            charset=CHARSET)

POSTGRES_URL = "postgresql+psycopg2://{user}:{password}@{host}/{database}".format(
    user=USER,
    password=PASSWORD,
    host=HOST,
    database=DB
)

def init_session(server_type='mysql', server_echo=True):
    if server_type == 'mysql':
        engine = create_engine(MYSQL_URL, encoding='utf-8', echo=server_echo)
    else:
        engine = create_engine(POSTGRES_URL, encoding='utf-8', echo=server_echo)

    from models import Base
    Base.metadata.create_all(engine)

    Session = sessionmaker()
    Session.configure(bind=engine)

    return Session
