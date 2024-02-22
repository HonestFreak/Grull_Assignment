from db.models.quests import Quest
from schemas.quests import questCreate
from sqlalchemy.orm import Session
from db.models.users import Manager
import json

def create_new_quest(quest: questCreate, db: Session, owner_id: int):
    Quest_object = Quest(**quest.dict(), owner_id=owner_id)
    db.add(Quest_object)
    db.commit()
    db.refresh(Quest_object)
    
    # Update tasks_created field of Villager
    manager = db.query(Manager).filter(Manager.id == owner_id).first()
    manager_tasks_str = manager.quests_created or "[]"
    manager_quests = json.loads(manager_tasks_str)
    manager_quests.append(Quest_object.id)
    manager.quests_created = json.dumps(manager_quests)
    db.commit()
    db.refresh(Quest_object)
    return Quest_object


def retreive_quest(id: int, db: Session):
    item = db.query(Quest).filter(Quest.id == id).first()
    return item


def list_quests(db: Session):
    Quests = db.query(Quest).all()
    return Quests


def update_quest_by_id(id: int, Quest: questCreate, db: Session, owner_id):
    existing_Quest = db.query(Quest).filter(Quest.id == id)
    if not existing_Quest.first():
        return "Quest with this id does not exist"
    Quest.__dict__.update(
        owner_id=owner_id
    )  # update dictionary with new key value of owner_id
    existing_Quest.update(Quest.__dict__)
    db.commit()
    return 1


def delete_quest_by_id(id: int, db: Session, owner_id):
    existing_Quest = db.query(Quest).filter(Quest.id == id)
    if not existing_Quest.first():
        return 0
    existing_Quest.delete(synchronize_session=False)
    db.commit()
    return 1


def search_quest(query: str, db: Session):
    Quests = db.query(Quest).filter(Quest.name.contains(query))
    return Quests
