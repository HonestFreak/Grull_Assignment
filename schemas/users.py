from typing import List, Dict, Any
from pydantic import BaseModel, EmailStr

# properties required during user creation
class UserCreate(BaseModel):
    name: str
    email: EmailStr
    password: str
    specializations: List[str]

class UserUpdate(BaseModel):
    password: str

class ShowUser(BaseModel):
    name: str
    email: EmailStr
    specializations: List[str]
    points: int
    quests: List[Dict[str, Any]]

    class Config:
        orm_mode = True

class ManagerCreate(BaseModel):
    name: str
    email: EmailStr
    password: str

class ManagerUpdate(BaseModel):
    password: str

class ShowManager(BaseModel):
    name: str
    email: EmailStr
    quests_created: List[Dict[str, Any]]

    class Config:
        orm_mode = True

class VillagerCreate(BaseModel):
    name: str
    email: EmailStr
    password: str

class VillagerUpdate(BaseModel):
    password: str

class ShowVillager(BaseModel):
    name: str
    email: EmailStr
    tasks_created: List[Dict[str, Any]]

    class Config:
        orm_mode = True
