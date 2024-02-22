from db.models.requests import Request
from db.models.users import User
from schemas.requests import requestCreate
from sqlalchemy.orm import Session
import json


def create_new_request(request: requestCreate, db: Session, owner_id: int):
    request_object = Request(**request.dict())
    db.add(request_object)
    db.commit()
    db.refresh(request_object)

    user = db.query(User).filter(User.id == owner_id).first()
    user_requests_str = user.requests_created or "[]"
    user_requests = json.loads(user_requests_str)
    print(request_object.owner_id)
    user_requests.append(request_object.id)
    user.requests_created = json.dumps(user_requests)
    db.commit()
    db.refresh(request_object)
    return request_object



def retreive_request(id: int, db: Session):
    item = db.query(Request).filter(Request.id == id).first()
    return item


def list_requests(db: Session):
    requests = db.query(Request).all()
    return requests


def update_request_by_id(id: int, request: requestCreate, db: Session, owner_id):
    existing_request = db.query(request).filter(request.id == id)
    if not existing_request.first():
        return "request with this id does not exist"
    request.__dict__.update(
        owner_id=owner_id
    )  # update dictionary with new key value of owner_id
    existing_request.update(request.__dict__)
    db.commit()
    return 1


def delete_request_by_id(id: int, db: Session, owner_id):
    existing_request = db.query(Request).filter(Request.id == id)
    if not existing_request.first():
        return 0
    existing_request.delete(synchronize_session=False)
    db.commit()
    return 1


def search_request(query: str, db: Session):
    requests = db.query(Request).filter(Request.name.contains(query))
    return requests
