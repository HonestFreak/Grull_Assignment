from datetime import date
from datetime import datetime
from typing import Optional

from pydantic import BaseModel


# shared properties
class questBase(BaseModel):
    id : Optional[int] = None
    title : Optional[str] = None
    description : Optional[str] = None
    completion_point : Optional[float] = None
    tasks : Optional[dict] = None

# this will be used to validate data while creating a quest
class questCreate(questBase):
    title : Optional[str] = None
    description : Optional[str] = None
    completion_point : Optional[float] = None
    tasks : Optional[dict] = None

# this will be used to format the response to not to have id,owner_id etc
class Showquest(questBase):
    id : Optional[int] = None
    title : Optional[str] = None
    description : Optional[str] = None
    completion_point : Optional[float] = None
    tasks : Optional[dict] = None

