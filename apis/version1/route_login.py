from datetime import timedelta
from fastapi import APIRouter, Depends, HTTPException, Response, status
from fastapi.security import OAuth2PasswordRequestForm
from jose import jwt, JWTError
from sqlalchemy.orm import Session
from schemas.tokens import Token
from db.repository.login import get_user, get_manager, get_villager
from db.session import get_db
from core.config import settings
from core.hashing import Hasher
from core.security import create_access_token
from apis.utils import OAuth2PasswordBearerWithCookie

router = APIRouter()

def get_user_by_role(username: str, role: str, db: Session):
    if role == "user":
        return get_user(username=username, db=db)
    elif role == "manager":
        return get_manager(username=username, db=db)
    elif role == "villager":
        return get_villager(username=username, db=db)
    return None

def authenticate_user(username: str, password: str, role: str, db: Session = Depends(get_db)):
    user = get_user_by_role(username, role, db)
    if not user or not Hasher.verify_password(password, user.hashed_password):
        return False
    return user

@router.post("/token", response_model=Token)
def login_for_access_token(
    response: Response,
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db),
    role: str = "user"
):
    user = authenticate_user(form_data.username, form_data.password, role, db)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
        )
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.email}, expires_delta=access_token_expires
    )
    response.set_cookie(
        key="access_token", value=f"Bearer {access_token}", #httponly=True
    )

    return {"access_token": access_token, "token_type": "bearer"}

oauth2_scheme = OAuth2PasswordBearerWithCookie(tokenUrl="/login/token")

def get_current_user_from_token(
    token: str = Depends(oauth2_scheme),
    role: str = "user",
    db: Session = Depends(get_db)
):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
    )
    try:
        payload = jwt.decode(
            token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM]
        )
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
        
    except JWTError:
        raise credentials_exception
    
    if role=="user" : 
        user = get_user(username=username, db=db)
    elif role=="manager" : 
        user = get_manager(username=username, db=db)
    elif role=="villager" :
        user = get_villager(username=username, db=db)
        
    return user  # Return the username instead of the user object
