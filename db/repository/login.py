from db.models.users import User
from db.models.users import Manager
from db.models.users import Villager
from db.models.users import Manager
from db.models.users import Villager
from sqlalchemy.orm import Session


def get_user(username: str, db: Session):
    user = db.query(User).filter(User.email == username).first()
    return user

def get_manager(username: str, db: Session):
    user = db.query(Manager).filter(Manager.email == username).first()
    return user

def get_villager(username: str, db: Session):
    user = db.query(Villager).filter(Villager.email == username).first()
    return user
