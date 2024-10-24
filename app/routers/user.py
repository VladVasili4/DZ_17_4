from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.orm import Session
from backend.db_depends import get_db
from typing import Annotated
from models import User, Task
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
    user_with_id = db.scalars(select(User).where(User.id == user_id)).first()
    if user_with_id is None:
        raise HTTPException(status_code=404, detail='User was not found')
    return user_with_id


@router.get ("/user_id/tasks")
async def user_by_id(db: Annotated[Session, Depends(get_db)], user_id: int):
    user_with_id = db.scalars(select(User).where(User.id == user_id)).first()
    if user_with_id is None:
        raise HTTPException(status_code=404, detail='User was not found')

    db.scalars(select(Task).where(Task.user_id == user_id))
    return {"user_id": user_with_id.id, "tasks": [task for task in user_with_id.tasks]}



@router.post('/create')
async def create_user(db: Annotated[Session, Depends(get_db)], cre_user: CreateUser):
    exist_user = db.execute(select(User).where(User.username == cre_user.username)).first()
    if exist_user:
        raise HTTPException(status_code=400, detail="User with this username already exists")

    db.execute(insert(User).values(username=cre_user.username,
                                   firstname=cre_user.firstname,
                                   lastname=cre_user.lastname,
                                   age=cre_user.age,
                                   slug=slugify(cre_user.username)))
    db.commit()
    return {'status_code': status.HTTP_201_CREATED, 'transaction': 'Successful'}



@router.put('/update')
async def update_user(db: Annotated[Session, Depends(get_db)], user_id: int, up_user: UpdateUser ):
    user_with_id = db.scalars(select(User).where(User.id == user_id)).first()
    if user_with_id is None:
        raise HTTPException(status_code=404, detail='User was not found')

    db.execute(update(User).where(User.id == user_id).values(firstname=up_user.firstname,
                                                              lastname=up_user.lastname,
                                                              age=up_user.age))
    db.commit()
    return {'status_code': status.HTTP_200_OK, 'transaction': 'User update is successful!'}





@router.delete('/delete')
async def delete_user(db: Annotated[Session, Depends(get_db)], user_id: int):
    user_del = db.scalars(select(User).where(User.id == user_id)).first()
    if user_del is None:
        raise HTTPException(status_code=404, detail='User was not found')

    db.execute(delete(Task).where(Task.user_id == user_id))
    db.execute(delete(User).where(User.id == user_id))
    db.commit()
    return {'status_code': status.HTTP_200_OK, 'transaction': 'User was deleted successful!'}


# uvicorn main:app


