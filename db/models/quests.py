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

# a quest is a collection of tasks
class Quest(Base):
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String ,default="")
    description = Column(String ,default="")
    completion_point = Column(Float ,default=0)
    tasks = Column(JSON, default="{}", nullable=False)
    owner_id = Column(Integer, ForeignKey("manager.id"))
    owner = relationship("Manager", back_populates="quests")