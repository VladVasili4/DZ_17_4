from backend.db import Base
from sqlalchemy import Integer, Column, String, Boolean, ForeignKey # ForeignKey - ключ для связывания таблиц
from sqlalchemy.orm import relationship
from sqlalchemy.schema import CreateTable
from models import *         # !!!! Это ВАЖНО! чтобы таблицы видели друг друга, т.к. они в разных файлах

class Task(Base):
    __tablename__ = 'tasks'
    __table_args__ = {'extend_existing': True}

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String)
    content = Column(String)
    priority = Column(Integer, default=0)
    completed = Column(Boolean, default=False)
    slug = Column(String, unique=True, index=True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False, index=True)

    user = relationship('User', back_populates='tasks')


print(CreateTable(Task.__table__))