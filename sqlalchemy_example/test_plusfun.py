# coding=utf-8
from sqlalchemy import Column
from sqlalchemy import DateTime
from sqlalchemy import func
from sqlalchemy import Integer
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column
from sqlalchemy import String
from sqlalchemy import Integer
from sqlalchemy import Text
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship, backref
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

MYSQL_USER     = 'root'
MYSQL_PASSWORD = '7VuNSOTKEFE6w7'
MYSQL_HOST     = '127.0.0.1'
MYSQL_PORT     = '3309'
MYSQL_DB       = 'plusfun'
MYSQL_CHARSET  = 'utf8' # it it import to automatically convert(encode/decode) data to unicode using utf8
MYSQL_URI      = 'mysql://{user}:{password}@{host}:{port}/{database}?charset={charset}'
mysql_uri = MYSQL_URI.format(user     = MYSQL_USER,
                        password = MYSQL_PASSWORD,
                        host     = MYSQL_HOST,
                        port     = MYSQL_PORT,
                        database = MYSQL_DB,
                        charset  = MYSQL_CHARSET
                        )
print(mysql_uri)
engine = create_engine(mysql_uri, encoding='utf-8', echo=True)


Session = sessionmaker(bind=engine)
Base = declarative_base(bind=engine)

class TimeStampedModel:
    """
    An abstract base class model that provides self-updating
    ``created`` and ``modified`` fields.

    """

    created = Column(DateTime(timezone=False),
                     default=func.now(),
                     server_default=func.now(),
                     nullable=False)
    modified = Column(DateTime(timezone=False),
                      default=func.now(),
                      server_default=func.now(),
                      onupdate=func.now(),
                      nullable=False)


class IDModel:
    id = Column(Integer, primary_key=True)


class Regulations(Base, TimeStampedModel, IDModel):
    __tablename__ = 'regulations'
    reg_url = Column(String(60), default='http://plusfun-domain.com/publish/regulations', nullable=False)
    reg_current_version = Column(String(10), default='0.0.1', nullable=False)
    reg_content = Column(Text, default='regulations content', nullable=False)
    sms_portal = Column(String(20), default='80090', nullable=False)

class UserConfig(Base, TimeStampedModel, IDModel):
    __tablename__ = 'user_config'

    platform_name = Column(String(30), default='', nullable=False)
    refresh_period = Column(Integer, default=24, nullable=False)
    min_app_version = Column(String(10), default='0.0.1', nullable=False)
    rec_app_version = Column(String(10), default='0.0.1', nullable=False)
    cur_app_version = Column(String(10), default='0.0.1', nullable=False)

    # reg_url = Column(String(60), default='http://plufun.com/someregulation.html', nullable=False)
    # reg_current_version = Column(String(10), default='0.0.1', nullable=False)
    regulations_id = Column(Integer, ForeignKey('regulations.id', ondelete='CASCADE'))
    regulations = relationship('Regulations', backref='clients')

    reporting_gstream_service = Column(String(25), default='', nullable=False)
    reporting_gstream_accounts = Column(String(100), default='', nullable=False)

    reporting_audience_service = Column(String(25), default='', nullable=False)
    reporting_audience_accounts = Column(String(100), default='', nullable=False)

    refresh_list_video_period = Column(Integer, default=5, nullable=False)
    what_new = Column(Text, default="new version description", nullable=False)

s = Session()
# s.add_all([u1, u2])
# s.commit()

# ================ read data =======================
for user in s.query(UserConfig):
    print(user.what_new)

# ================ save data =======================
# for user in s.query(UserConfig):
#     user.what_new = 'được đấy'
#     print(user.what_new)
# s.commit()

