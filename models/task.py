#!/usr/bin/env python3
"""Base class task. This class maps to the 'tasks' table."""

from models.base import Base, Activity
from sqlalchemy import Column, ForeignKey, String


class Task(Activity, Base):
    """Base class for Activity. This class maps to the 'Activities' table."""

    __tablename__ = "tasks"
    task_name = Column(String(16), nullable=False)
    user_id = Column(String(60), ForeignKey("users.id"), nullable=False)
    task_date = Column(String(16), nullable=False)
    task_time = Column(String(16), nullable=False)
    # task_status = Column(String(16), nullable=True)

# task status it can be default value Done or Undone base on checkbox in task card 

