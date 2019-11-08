from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker


PASSWORD = '123456'
HOST = 'localhost'

MYSQL_USER = 'root'
MYSQL_PORT = 3308

POSTGRES_USER = 'postgres'
POSTGRES_PORT = 5433

DB = 'test_database'

CHARSET = 'utf8'  # NOTE: it import to automatically convert(encode/decode) data to unicode using utf8
MYSQL_URL = 'mysql+pymysql://{user}:{password}@{host}:{port}/{database}?charset={charset}'\
    .format(user=MYSQL_USER,
            password=PASSWORD,
            host=HOST,
            port=MYSQL_PORT,
            database=DB,
            charset=CHARSET)

POSTGRES_URL = "postgresql+psycopg2://{user}:{password}@{host}:{port}/{database}".format(
    user=POSTGRES_USER,
    password=PASSWORD,
    host=HOST,
    port=POSTGRES_PORT,
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

    return Session, engine
