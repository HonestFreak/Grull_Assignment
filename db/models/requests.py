from db.base_class import Base
from sqlalchemy import Boolean
from sqlalchemy import Column
from sqlalchemy import Date
from sqlalchemy import ForeignKey
from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy.orm import relationship
from sqlalchemy import JSON
from sqlalchemy import Float

class Request(Base):
    id = Column(Integer, primary_key=True, index=True)
    requested_quest = Column(Integer, ForeignKey('quest.id'))
    owner_id = Column(Integer, ForeignKey('user.id'))
    accepted = Column(Boolean, default=False)
    completed = Column(Boolean, default=False)
    start_date = Column(Date)
