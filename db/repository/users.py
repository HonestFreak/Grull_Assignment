from core.hashing import Hasher
from db.models.users import User
from db.models.users import Manager
from db.models.users import Villager
from schemas.users import UserCreate
from sqlalchemy.orm import Session
from schemas.users import UserUpdate
from schemas.users import ManagerCreate
from schemas.users import ManagerUpdate
from schemas.users import VillagerCreate
from schemas.users import VillagerUpdate

def create_new_user(user: UserCreate, db: Session):
    user = User(
        name=user.name,
        email=user.email,
        hashed_password=Hasher.get_password_hash(user.password),
        specializations = user.specializations,
        points = 0,
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return user

def create_new_manager(user: ManagerCreate, db: Session):
    manager = Manager(
        name=user.name,
        email=user.email,
        hashed_password=Hasher.get_password_hash(user.password),
        quests_created = {},
    )
    db.add(manager)
    db.commit()
    db.refresh(manager)
    return manager

def create_new_villager(villager: UserCreate, db: Session):
    villager = Villager(
        name=villager.name,
        email=villager.email,
        hashed_password=Hasher.get_password_hash(villager.password),
        tasks_created = {},
    )
    db.add(villager)
    db.commit()
    db.refresh(villager)
    return villager


def get_user_by_email(email: str, db: Session):
    user = db.query(User).filter(User.email == email).first()
    return user
