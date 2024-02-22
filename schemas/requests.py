from datetime import date
from datetime import datetime
from typing import Optional

from pydantic import BaseModel


# shared properties
class requestBase(BaseModel):
    id : Optional[int] = None
    requested_quest : Optional[int] = None
    owner_id : Optional[int] = None
    accepted : Optional[bool] = None
    completed : Optional[bool] = None
    start_date : Optional[date] = None

# this will be used to validate data while creating a request
class requestCreate(requestBase):
    requested_quest : Optional[int] = None
    owner_id : Optional[int] = None
    accepted : Optional[bool] = None
    completed : Optional[bool] = None
    start_date : Optional[date] = None

# this will be used to format the response to not to have id,owner_id_id etc
class Showrequest(requestBase):
    id : Optional[int] = None
    requested_quest : Optional[int] = None
    owner_id : Optional[int] = None
    accepted : Optional[bool] = None
    completed : Optional[bool] = None
    start_date : Optional[date] = None

