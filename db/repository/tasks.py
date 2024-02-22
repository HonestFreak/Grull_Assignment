from db.models.tasks import Task
from db.models.users import Villager
from schemas.tasks import taskCreate
from sqlalchemy.orm import Session
import json


def create_new_task(task: taskCreate, db: Session, owner_id: int):
    task_object = Task(**task.dict(), owner_id=owner_id)
    db.add(task_object)
    db.commit()
    db.refresh(task_object)

    villager = db.query(Villager).filter(Villager.id == owner_id).first()
    villager_tasks_str = villager.tasks_created or "[]"
    villager_tasks = json.loads(villager_tasks_str)
    print(task_object.owner_id)
    villager_tasks.append(task_object.id)
    villager.tasks_created = json.dumps(villager_tasks)
    db.commit()
    db.refresh(task_object)
    return task_object



def retreive_task(id: int, db: Session):
    item = db.query(Task).filter(Task.id == id).first()
    return item


def list_tasks(db: Session):
    tasks = db.query(Task).all()
    return tasks


def update_task_by_id(id: int, task: taskCreate, db: Session, owner_id):
    existing_task = db.query(task).filter(task.id == id)
    if not existing_task.first():
        return "task with this id does not exist"
    task.__dict__.update(
        owner_id=owner_id
    )  # update dictionary with new key value of owner_id
    existing_task.update(task.__dict__)
    db.commit()
    return 1


def delete_task_by_id(id: int, db: Session, owner_id):
    existing_task = db.query(Task).filter(Task.id == id)
    if not existing_task.first():
        return 0
    existing_task.delete(synchronize_session=False)
    db.commit()
    return 1


def search_task(query: str, db: Session):
    tasks = db.query(Task).filter(Task.name.contains(query))
    return tasks
