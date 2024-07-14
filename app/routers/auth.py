
from fastapi import APIRouter, Depends, status, HTTPException, exceptions, Path
from settings import SesscionLocal
from typing import Annotated
from sqlalchemy.orm import Session
from models import Supplier
from pydantic import BaseModel, Field
from socket import gethostname, gethostbyname
from datetime import datetime, timedelta
from jose import jwt, JWTError
from passlib.context import CryptContext


router = APIRouter(
    prefix='/auth',
    tags=['auth']
)


def get_db_conn():
    db = SesscionLocal()
    try:
        yield db
    finally:
        db.close()


db_dependency = Annotated[Session, Depends(get_db_conn)]


ALGORITHM = 'HS256'
SECRET_KEY = 'tcj1$f3k2z0%^6%0h=+g*%@2*u6+zu@m^j7dh-6*2lu44ka*p0'
pwd_context = CryptContext(schemes=['bcrypt'])

def create_access_token(username: str, user_id: int, user_rol: str, expires_delta: timedelta):
    encode = {
        'sub': username,
        'id': user_id,
    }

    expire = datetime.now() + expires_delta

    encode.update({
        'exp': expire
    })

    return jwt.encode(encode, key=SECRET_KEY, algorithm=ALGORITHM)


def authenticate_user(db: db_dependency, user_name: str, password: str):
    user = db.query(Supplier).filter(Supplier.user_name == user_name).first()

    if not user:
        return False
    if not pwd_context.verify(password, user.password):
        return False

    return user