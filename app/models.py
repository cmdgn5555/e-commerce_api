
from settings import Base
from sqlalchemy import Integer, Column, String


class Category(Base):
    __tablename__ = 'store_category'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    slug = Column(String, unique=True)
    status = Column(String)
    ip_address = Column(String)
    machine_name = Column(String)


class Supplier(Base):
    __tablename__ = 'store_supplier'

    id = Column(Integer, primary_key=True, index=True)
    companyname = Column(String, unique=True)
    user_name = Column(String, unique=True)
    password = Column(String)
    status = Column(String)
    ip_address = Column(String)
    machine_name = Column(String)