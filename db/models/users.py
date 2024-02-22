from db.base_class import Base
from sqlalchemy import Column, Integer, String, JSON, Float
from sqlalchemy.orm import relationship
from sqlalchemy import ForeignKey

class User(Base):
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    email = Column(String, nullable=False, unique=True, index=True)
    hashed_password = Column(String, nullable=False)
    specializations = Column(JSON, default={}, nullable=False)
    points = Column(Integer, default=0)
    requests_created = Column(JSON, default={}, nullable=False) 

class Manager(Base):
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, nullable=False)
    email = Column(String, nullable=False, unique=True, index=True)
    hashed_password = Column(String, nullable=False)
    quests_created = Column(JSON, nullable=False)  
    quests = relationship("Quest", back_populates="owner")

class Villager(Base):
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, nullable=False)
    email = Column(String, nullable=False, unique=True, index=True)
    hashed_password = Column(String, nullable=False)
    tasks_created = Column(JSON, nullable=False)  
    tasks = relationship("Task", back_populates="owner")
