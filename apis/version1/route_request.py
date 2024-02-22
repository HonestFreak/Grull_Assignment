from typing import List
from typing import Optional

from apis.version1.route_login import get_current_user_from_token
from db.models.users import User
from db.repository.requests import create_new_request
from db.repository.requests import delete_request_by_id
from db.repository.requests import list_requests
from db.repository.requests import retreive_request
from db.repository.requests import search_request
from db.repository.requests import update_request_by_id
from db.session import get_db
from fastapi import APIRouter
from fastapi import Depends
from fastapi import HTTPException
from fastapi import status
from schemas.requests import requestCreate
from schemas.requests import Showrequest
from sqlalchemy.orm import Session


router = APIRouter()


@router.post("/create-request/")
def create_request(
    request: requestCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user_from_token),
):
    request = create_new_request(request=request, db=db, owner_id=current_user.id)
    return request


@router.get(
    "/get/{id}", response_model=Showrequest
)  # if we keep just "{id}" . it would stat catching all routes
def read_request(id: int, db: Session = Depends(get_db)):
    request = retreive_request(id=id, db=db)
    if not request:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"request with this id {id} does not exist",
        )
    return request


@router.get("/all", response_model=List[Showrequest])
def read_requests(db: Session = Depends(get_db)):
    requests = list_requests(db=db)
    return requests


@router.put("/update/{id}")
def update_request(id: int, request: requestCreate, db: Session = Depends(get_db)
               , current_user: User = Depends(get_current_user_from_token)):
    message = update_request_by_id(id=id, request=request, db=db, owner_id=current_user.id)
    if not message:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=f"request with id {id} not found"
        )
    return {"msg": "Successfully updated data."}


@router.delete("/delete/{id}")
def delete_request(
    id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user_from_token),
):
    request = retreive_request(id=id, db=db)
    if not request:
        return HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"request with id {id} does not exist",
        )
    print(request.owner_id, current_user.id, current_user.is_superuser)
    if request.owner_id == current_user.id or current_user.is_superuser:
        delete_request_by_id(id=id, db=db, owner_id=current_user.id)
        return {"detail": "Successfully deleted."}
    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED, detail="You are not permitted!!!!"
    )
