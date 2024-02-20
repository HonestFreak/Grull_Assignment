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

class Task(Base):
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, default="")
    location = Column(String, default="")
    description = Column(String, default="")
    reward = Column(Float, default="")
    owner_id = Column(Integer, ForeignKey("villager.id"))
    owner = relationship("Villager", back_populates="tasks")
