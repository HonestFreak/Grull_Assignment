from db.base_class import Base
from sqlalchemy import Column, Integer, String, JSON, Float
from sqlalchemy.orm import relationship

class User(Base):
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, nullable=False)
    email = Column(String, nullable=False, unique=True, index=True)
    hashed_password = Column(String, nullable=False)
    specializations = Column(JSON, nullable=False)
    points = Column(Integer, default=0)
    quests = Column(JSON, default={}, nullable=False)  # Use {} instead of "{}"
    # quest: {"quest_id": {"completed": True, "date_started": "2021-10-10", "date_completed": "2021-10-10"}}

class Manager(Base):
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, nullable=False)
    email = Column(String, nullable=False, unique=True, index=True)
    hashed_password = Column(String, nullable=False)
    quests_created = Column(JSON, default={}, nullable=False)  # Use {} instead of "{}"
    quests = relationship("Quest", back_populates="owner")

class Villager(Base):
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, nullable=False)
    email = Column(String, nullable=False, unique=True, index=True)
    hashed_password = Column(String, nullable=False)
    tasks_created = Column(JSON, default={}, nullable=False)  # Use {} instead of "{}"
    tasks = relationship("Task", back_populates="owner")