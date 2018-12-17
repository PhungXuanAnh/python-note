from sqlalchemy import Column, DateTime, String, Integer, func, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

Base = declarative_base()


class RootCause(Base):
    __tablename__ = 'root_cause'
    id = Column(Integer, primary_key=True)
    name = Column(String)


class Bug(Base):
    __tablename__ = 'bug'
    id = Column(Integer, primary_key=True)
    root_cause_id = Column(ForeignKey('root_cause.id'),
                           nullable=False,
                           index=True)
    bug_tracker_url = Column(String, unique=True)
    who = Column(String)
    when = Column(DateTime, default=func.now())

    root_cause = relationship(RootCause)

    def __repr__(self):
        return 'id: {}, root cause: {}'.format(self.id, self.root_cause.name)
