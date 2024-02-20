from apis.version1 import route_tasks
from apis.version1 import route_login
from apis.version1 import route_users
from apis.version1 import route_quests
from fastapi import APIRouter


api_router = APIRouter()
api_router.include_router(route_login.router, prefix="/login", tags=["login"])
api_router.include_router(route_users.router, prefix="/users", tags=["users"])
api_router.include_router(route_tasks.router, prefix="/tasks", tags=["tasks"])
api_router.include_router(route_quests.router, prefix="/quests", tags=["quests"])
# api_router.include_router(route_chat.router, prefix="/chat", tags=["chat"])
# api_router.include_router(route_collections.router, prefix="/collections", tags=["collections"])
# api_router.include_router(route_credit.router, prefix="/credit", tags=["credit"])

