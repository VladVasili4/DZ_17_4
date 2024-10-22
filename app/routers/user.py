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

@router.get('/{user_id}')
async def user_by_id(db: Annotated[Session, Depends(get_db)], user_id: int):
    user_with_id = db.scalars(select(User).where(User.id == user_id))
    if user_with_id is not None:
        return user_with_id
    raise HTTPException(status_code=404, detail='User was not found')

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
async def update_user(db: Annotated[Session, Depends(get_db)], user_id: int, up_user: UpdateUser ):
    user_with_id = db.scalars(select(User).where(User.id == user_id))
    if user_with_id is not None:
        db.execute(update(User).where(User.id == user_id).values(firstname=up_user.firstname,
                                                                  lastname=up_user.lastname,
                                                                  age=up_user.age))
        db.commit()
        return {'status_code': status.HTTP_200_OK, 'transaction': 'User update is successful!'}
    raise HTTPException(status_code=404, detail='User was not found')




@router.delete('/delete')
async def delete_user(db: Annotated[Session, Depends(get_db)], user_id: int):
    user_del = db.scalars(select(User).where(User.id == user_id))
    if user_del is not None:
        db.execute(delete(User).where(User.id == user_id))
        db.commit()
        return {'status_code': status.HTTP_200_OK, 'transaction': 'User was deleted successful!'}
    raise HTTPException(status_code=404, detail='User was not found')

# uvicorn main:app