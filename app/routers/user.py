from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.orm import Session
from backend.db_depends import get_db
from typing import Annotated
from models import User
from sqlalchemy import insert, select, delete, update
from schemas import CreateUser, UpdateUser

from slugify import slugify

router = APIRouter(prefix='/user', tags=['user'])


@router.get('/')
async def all_users(db: Annotated[Session, Depends(get_db)]):
    users_all = db.scalars(select(User)).all()
    return users_all

@router.get('/user_id')
async def user_by_id(db: Annotated[Session, Depends(get_db)], user_id: int):
    try:
        user_with_id = db.scalars(select(User).where(User.id == user_id))
        return user_with_id
    except IndexError:
        raise HTTPException(status_code=404, detail='Message Not found')

@router.post('/create')        # Здесь надо еще проверить на наличие такого юзера в базе. Вдруг он уже есть.
async def create_user(db: Annotated[Session, Depends(get_db)], create_user_m: CreateUser):
    db.execute(insert(User).values(username=create_user_m.username,
                                   firstname=create_user_m.firstname,
                                   lastname=create_user_m.lastname,
                                   age=create_user_m.age,
                                   slug=slugify(create_user_m.username)))
    db.commit()
    return {'status_code': status.HTTP_201_CREATED, 'transaction': 'Successful'}



@router.put('/update')
async def update_user(db: Annotated[Session, Depends(get_db)]):
    pass


@router.delete('/delete')
async def delete_user(db: Annotated[Session, Depends(get_db)]):
    pass