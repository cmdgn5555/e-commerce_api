
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

SQLALCHEMY_DATABASE_URL = 'sqlite:///C:/Users/Kurumsal/PycharmProjects/ecommerce/ecommerce/db.sqlite3'


engine = create_engine(
    url=SQLALCHEMY_DATABASE_URL,
    connect_args={
        'check_same_thread': False
    }
)

SesscionLocal = sessionmaker(
    autoflush=False,
    autocommit=False,
    bind=engine
)

Base = declarative_base()