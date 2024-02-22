from typing import List
from typing import Optional

from apis.version1.route_login import get_current_user_from_token
from db.models.users import User
from db.repository.tasks import create_new_task
from db.repository.tasks import delete_task_by_id
from db.repository.tasks import list_tasks
from db.repository.tasks import retreive_task
from db.repository.tasks import search_task
from db.repository.tasks import update_task_by_id
from db.session import get_db
from fastapi import APIRouter
from fastapi import Depends
from fastapi import HTTPException
from fastapi import status
from schemas.tasks import taskCreate
from schemas.tasks import Showtask
from sqlalchemy.orm import Session


router = APIRouter()


@router.post("/create-task/")
def create_task(
    task: taskCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user_from_token),
):
    task = create_new_task(task=task, db=db, owner_id=current_user.id)
    return task


@router.get(
    "/get/{id}", response_model=Showtask
)  # if we keep just "{id}" . it would stat catching all routes
def read_task(id: int, db: Session = Depends(get_db)):
    task = retreive_task(id=id, db=db)
    if not task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"task with this id {id} does not exist",
        )
    return task


@router.get("/all", response_model=List[Showtask])
def read_tasks(db: Session = Depends(get_db)):
    tasks = list_tasks(db=db)
    return tasks


@router.put("/update/{id}")
def update_task(id: int, task: taskCreate, db: Session = Depends(get_db)
               , current_user: User = Depends(get_current_user_from_token)):
    message = update_task_by_id(id=id, task=task, db=db, owner_id=current_user.id)
    if not message:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=f"task with id {id} not found"
        )
    return {"msg": "Successfully updated data."}


@router.delete("/delete/{id}")
def delete_task(
    id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user_from_token),
):
    task = retreive_task(id=id, db=db)
    if not task:
        return HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"task with id {id} does not exist",
        )
    print(task.owner_id, current_user.id, current_user.is_superuser)
    if task.owner_id == current_user.id or current_user.is_superuser:
        delete_task_by_id(id=id, db=db, owner_id=current_user.id)
        return {"detail": "Successfully deleted."}
    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED, detail="You are not permitted!!!!"
    )


@router.get("/autocomplete")
def autocomplete(term: Optional[str] = None, db: Session = Depends(get_db)):
    tasks = search_task(term, db=db)
    task_titles = []
    for task in tasks:
        task_titles.append(task.title)
    return task_titles
