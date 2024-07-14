
from fastapi import APIRouter, Depends, status, HTTPException, exceptions, Path
from settings import SesscionLocal
from typing import Annotated
from sqlalchemy.orm import Session
from models import Category
from pydantic import BaseModel, Field
from socket import gethostname, gethostbyname


router = APIRouter()


def get_db_conn():
    db = SesscionLocal()

    try:
        yield db
    except exceptions as exp:
        print(exp)
    finally:
        db.close()


db_dependency = Annotated[Session, Depends(get_db_conn)]


class CategoryDTO(BaseModel):
    name: str


@router.post(path='/category/create', status_code=status.HTTP_201_CREATED)
async def create_category(db: db_dependency, category_dto: CategoryDTO):
    model = Category()

    model.name = category_dto.name
    model.slug = category_dto.name.lower().replace(' ', '-')
    model.status = 'Active'
    model.machine_name = gethostname()
    model.ip_address = gethostbyname(gethostname())

    db.add(model)
    db.commit()

    return {
        'status_code': 201,
        'transaction': 'Successful'
    }


@router.get(path='/', status_code=status.HTTP_200_OK)
async def get_all_categories(db: db_dependency):
    data = db.query(Category).all()

    if data is not None:
        return data

    raise HTTPException(
        status_code=404,
        detail='There is no data'
    )


@router.get(path='/category/{category_id}',
            status_code=status.HTTP_200_OK,
            summary='This function get category by id information',
            description='This function get category via id information, id must be integer and greater than zero')
async def get_category_by_id(db: db_dependency, category_id: int = Path(gt=0)):
    data = db.query(Category).filter(Category.id == category_id).first()

    if data is not None:
        return data

    raise HTTPException(
        status_code=404,
        detail='Category not found'
    )


@router.put(path='/category/{category_id}',
            status_code=status.HTTP_200_OK,
            summary='This method updated single category',
            description='This method updated single category, you must to filter by id and send information by DTO so please check schemas tab')
async def update_category(db: db_dependency,
                          category_dto: CategoryDTO,
                          category_id: int = Path(gt=0)):
    data = db.query(Category).filter(Category.id == category_id).first()

    if data is None:
        raise HTTPException(
            status_code=404,
            detail='Category not found'
        )

    if db is None:
        raise HTTPException(
            status_code=500,
            detail='Database can not be reach'
        )

    data.name = category_dto.name
    data.slug = category_dto.name.lower().replace(' ', '-')
    data.status = 'Modified'
    data.machine_name = gethostname()
    data.ip_address = gethostbyname(gethostname())

    db.add(data)
    db.commit()

    return {
        'status_code': 200,
        'transaction': 'Successfull'
    }


@router.delete(path='/category/{category_id}', status_code=status.HTTP_200_OK)
async def delete_category(db: db_dependency,
                          category_id: int = Path(gt=0)):
    data = db.query(Category).filter(Category.id == category_id).first()

    if data is None:
        raise HTTPException(
            status_code=404,
            detail='Category not found'
        )

    if db is None:
        raise HTTPException(
            status_code=500,
            detail='Database can not be reach'
        )

    data.status = 'Passive'
    data.machine_name = gethostname()
    data.ip_address = gethostbyname(gethostname())

    db.add(data)
    db.commit()

    return {
        'status_code': 200,
        'transaction': 'Successfull'
    }
