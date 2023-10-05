#!/usr/bin/env python3

from models.base import Base, Activity
from sqlalchemy import Column, String
from sqlalchemy.orm import relationship


class User(Activity, Base):
    """Base class for Activity. This class maps to the 'Activities' table."""

    __tablename__ = "users"
    name = Column(String(128), nullable=False)
    email = Column(String(128), nullable=False)
    password = Column(String(128), nullable=False)
    # task_status = Column(String(16), nullable=True)
    tasks = relationship(
        "Task", backref="users", cascade="all, delete, delete-orphan"
    )
