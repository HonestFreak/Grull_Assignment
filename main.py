from apis.base import api_router
from core.config import settings
from db.base import Base
from db.session import engine
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
# main


def include_router(app):
    app.include_router(api_router)

def create_tables():
    Base.metadata.create_all(bind=engine)


def start_application():
    app = FastAPI(title=settings.PROJECT_NAME, version=settings.PROJECT_VERSION)
    include_router(app)
    create_tables()
    return app


app = start_application()

origins = [
 # If deployed
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,  # Replace with your frontend's URL or "*" for all origins (not recommended for production)
    allow_credentials=True,
    allow_methods=["*"],  # Adjust the allowed HTTP methods as per your requirements
    allow_headers=["*"],  # Adjust the allowed headers as per your requirements
)

# @app.on_event("startup")
# async def app_startup():
#     await check_db_connected()


# @app.on_event("shutdown")
# async def app_shutdown():
#     await check_db_disconnected()

