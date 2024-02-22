from apis.version1 import route_tasks
from apis.version1 import route_login
from apis.version1 import route_users
from apis.version1 import route_quests
from apis.version1 import route_quest_search
from apis.version1 import route_request
from fastapi import APIRouter


api_router = APIRouter()
api_router.include_router(route_login.router, prefix="/login", tags=["login"])
api_router.include_router(route_users.router, prefix="/users", tags=["users"])
api_router.include_router(route_tasks.router, prefix="/tasks", tags=["tasks"])
api_router.include_router(route_quests.router, prefix="/quests", tags=["quests"])
api_router.include_router(route_request.router, prefix="/requests", tags=["requests"])
api_router.include_router(route_quest_search.router, prefix="/search", tags=["search"])
