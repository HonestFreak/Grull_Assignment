from datetime import date
from datetime import datetime
from typing import Optional

from pydantic import BaseModel


# shared properties
class taskBase(BaseModel):
    id : Optional[int] = None
    title : Optional[str] = None
    location : Optional[str] = None
    description : Optional[str] = None
    reward : Optional[float] = None

# this will be used to validate data while creating a task
class taskCreate(taskBase):
    title : Optional[str] = None
    location : Optional[str] = None
    description : Optional[str] = None
    reward : Optional[float] = None

# this will be used to format the response to not to have id,owner_id etc
class Showtask(taskBase):
    id : Optional[int] = None
    title : Optional[str] = None
    location : Optional[str] = None
    description : Optional[str] = None
    reward : Optional[float] = None

