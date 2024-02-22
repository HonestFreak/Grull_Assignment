from typing import List
from typing import Optional

from apis.version1.route_login import get_current_user_from_token
from db.models.users import User
from db.repository.quests import create_new_quest
from db.repository.quests import delete_quest_by_id
from db.repository.quests import list_quests
from db.repository.quests import retreive_quest
from db.repository.quests import search_quest
from db.repository.quests import update_quest_by_id
from db.session import get_db
from fastapi import APIRouter
from fastapi import Depends
from fastapi import HTTPException
from fastapi import status
from schemas.quests import questCreate
from schemas.quests import Showquest
from sqlalchemy.orm import Session


router = APIRouter()


@router.post("/create-quest/")
def create_quest(
    quest: questCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user_from_token),
):
    quest = create_new_quest(quest=quest, db=db, owner_id=current_user.id)
    return quest


@router.get(
    "/get/{id}", response_model=Showquest
)  # if we keep just "{id}" . it would stat catching all routes
def read_quest(id: int, db: Session = Depends(get_db)):
    quest = retreive_quest(id=id, db=db)
    if not quest:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"quest with this id {id} does not exist",
        )
    return quest


@router.get("/all", response_model=List[Showquest])
def read_quests(db: Session = Depends(get_db)):
    quests = list_quests(db=db)
    return quests


@router.put("/update/{id}")
def update_quest(id: int, quest: questCreate, db: Session = Depends(get_db)
               , current_user: User = Depends(get_current_user_from_token)):
    message = update_quest_by_id(id=id, quest=quest, db=db, owner_id=current_user.id)
    if not message:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=f"quest with id {id} not found"
        )
    return {"msg": "Successfully updated data."}


@router.delete("/delete/{id}")
def delete_quest(
    id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user_from_token),
):
    quest = retreive_quest(id=id, db=db)
    if not quest:
        return HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"quest with id {id} does not exist",
        )
    print(quest.owner_id, current_user.id, current_user.is_superuser)
    if quest.owner_id == current_user.id or current_user.is_superuser:
        delete_quest_by_id(id=id, db=db, owner_id=current_user.id)
        return {"detail": "Successfully deleted."}
    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED, detail="You are not permitted!!!!"
    )


@router.get("/autocomplete")
def autocomplete(term: Optional[str] = None, db: Session = Depends(get_db)):
    quests = search_quest(term, db=db)
    quest_titles = []
    for quest in quests:
        quest_titles.append(quest.title)
    return quest_titles
