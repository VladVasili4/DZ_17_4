from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.orm import Session
from backend.db_depends import get_db
from typing import Annotated
from models import Task, User
from sqlalchemy import insert, select, delete, update
from schemas import CreateTask, UpdateTask
from slugify import slugify

router = APIRouter(prefix='/task', tags=['task'])


@router.get('/')
async def all_tasks(db: Annotated[Session, Depends(get_db)]):
    task_all = db.scalars(select(Task)).all()
    return task_all

@router.get('/{task_id}')
async def task_by_id(db: Annotated[Session, Depends(get_db)], task_id: int):
    task_with_id = db.scalars(select(Task).where(Task.id == task_id)).first()
    if task_with_id is None:
        raise HTTPException(status_code=404, detail='Task was not found')

    return task_with_id


@router.post('/create')
async def create_task(db: Annotated[Session, Depends(get_db)], user_id: int, create_task_m: CreateTask):
    user_with_id = db.scalars(select(User).where(User.id == user_id)).first()
    if user_with_id is None:
        raise HTTPException(status_code=404, detail='User not found')

    db.execute(insert(Task).values(title=create_task_m.title,
                                   content=create_task_m.content,
                                   priority=create_task_m.priority,
                                   slug=slugify(create_task_m.title),
                                   user_id=user_id))
    db.commit()
    return {'status_code': status.HTTP_201_CREATED, 'transaction': 'Task created successfully!'}



@router.put('/update')
async def update_task(db: Annotated[Session, Depends(get_db)], task_id: int, up_task: UpdateTask ):
    task_up = db.scalars(select(Task).where(Task.id == task_id)).first()
    if task_up is None:
        raise HTTPException(status_code=404, detail='Task was not found')

    db.execute(update(Task).where(Task.id == task_id).values(title=up_task.title,
                                                             content=up_task.content,
                                                             priority=up_task.priority))
    db.commit()
    return {'status_code': status.HTTP_200_OK, 'transaction': 'Task update is successful!'}


@router.delete('/delete')
async def delete_task(db: Annotated[Session, Depends(get_db)], task_id: int):
    task_del = db.scalars(select(Task).where(Task.id == task_id)).first()
    if task_del is None:
        raise HTTPException(status_code=404, detail='Task not found')

    db.execute(delete(Task).where(Task.id == task_id))
    db.commit()
    return {'status_code': status.HTTP_200_OK, 'transaction': 'Task was deleted successful!'}





# uvicorn main:app