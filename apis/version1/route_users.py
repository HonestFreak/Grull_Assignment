from db.repository.users import create_new_user
from db.repository.users import create_new_manager
from db.repository.users import create_new_villager
from db.session import get_db
from fastapi import APIRouter
from fastapi import Depends
from schemas.users import ShowUser
from schemas.users import UserCreate
from sqlalchemy.orm import Session
from db.models.users import User
from db.models.users import Manager
from db.models.users import Villager
from apis.version1.route_login import get_current_user_from_token
import requests
import smtplib
import random
import datetime
from fastapi_utilities import repeat_every
from chromadb.config import Settings
import email.utils
import os

router = APIRouter()

HOST = os.getenv("HOST")
PORT = os.getenv("PORT")
FROM_EMAIL = os.getenv("FROM_EMAIL")
URL = os.getenv("URL")
PASSWORD = os.getenv("EMAIL_PASSWORD")

otp_list = {}

@router.on_event('startup')
@repeat_every(seconds=3600)
async def clean_otp():
    for i in otp_list:
        if datetime.datetime.now() > otp_list[i][2]:
            del otp_list[i]

@router.get("/verify/{email}/{code}")
def verify(code: int, email: str, db: Session = Depends(get_db)):
    user = otp_list[email][1]
    if code == otp_list[email][0] and datetime.datetime.now() < otp_list[email][3]:
        role = otp_list[email][2]
        if(role == "user"):
            new_user = create_new_user(user=user, db=db)
            return new_user
        elif(role == "manager"):
            new_user = create_new_manager(user=user, db=db)
            return new_user
        elif(role == "villager"):
            new_user = create_new_villager(villager=user, db=db)
            return new_user
        else:
            return {"msg": "invalid role"}
    else:
        return {"msg": "failed to verify email"}
    

@router.post("/signup_user")
def create_user(user: UserCreate, role: str):
    # send verification mail and verify 
    global otp_list
    code = random.randint(100000, 999999)
    try:
        message_id = email.utils.make_msgid()
        link = URL + "/users/verify/" + user.email + "/" + str(code)
        BODY = "\r\n".join((
            "From: %s" % FROM_EMAIL,
            "To: %s" % user.email,
            "Message-ID:" + message_id,
            "Subject: %s" % "Verification mail for GRULL" ,
            "",
            "Welcome to Grull!",
            "We are excited to have you on board. Please verify your email to continue. "
            "Follow the below link to verify : " + link,
            ))
        server = smtplib.SMTP(HOST, PORT)
        server.starttls()
        server.login(FROM_EMAIL, PASSWORD) 
        server.sendmail(FROM_EMAIL, user.email, BODY )
        server.quit()
        otp_list[user.email] = [code, user , role,
                                datetime.datetime.now() + datetime.timedelta(hours=1)]
        
    except Exception as e:
        print(e)
        print("Error: error while sending mail")
    return {"msg": "sent email to " + user.email}

@router.get("/userinfo")
def show_user(current_user: User = Depends(get_current_user_from_token), db: Session = Depends(get_db)):
    return current_user

@router.get("/notification")
def show_notification():
    return "hi there, this is a notification"

@router.post("/feedback")
def feedback(feedback: str ,current_user: User = Depends(get_current_user_from_token)):
    base_url = 'https://api.airtable.com/v0/app7LTqISx0a2RszS/feedback'
    headers = {'Authorization': 'Bearer keyPk9loTUSq1QHJA', 'Content-Type': 'application/json'}
    
    # Define the data to be sent in the request
    data = {
        'fields': {
            'email': current_user.email,
            'feedback': feedback
        }
    }
    
    # Send a POST request to update the table
    response = requests.post(base_url, headers=headers, json=data)
    
    if response.status_code == 200:
        print('Table updated successfully.')
    else:
        print('An error occurred while updating the table.')
        print(response.text)