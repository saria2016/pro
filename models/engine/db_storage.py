#!/usr/bin/env python3
"""module for the DBStorage class"""

from models.base import Base
from models.user import User
from models.task import Task

from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

clx = {
    "User": User,
    "Task": Task,
}


class DBStorage:
    """interaacts with the MySQL database"""

    __engine = None
    __session = None
    __usr = "task_admin"
    __pswd = "task_pwd"
    __db = "task_db"
    __host = "localhost"

    def __init__(self):
        """Instantiate a DBStorage object"""
        self.__engine = create_engine(
            "mysql+mysqldb://{}:{}@{}/{}".format(
                DBStorage.__usr,
                DBStorage.__pswd,
                DBStorage.__host,
                DBStorage.__db,
            ),
            pool_pre_ping=False,
            echo=False,
        )

    def all(self, cls=None):
        """query on the current database session"""
        new_dict = {}
        for clss in clx:
            if cls is None or cls is clx[clss] or cls is clss:
                objs = self.__session.query(clx[clss]).all()
                for obj in objs:
                    key = obj.__class__.__name__ + "." + obj.id
                    new_dict[key] = obj
        return new_dict

    def new(self, obj):
        """add the object to the current database session"""
        self.__session.add(obj)

    def save(self):
        """commit all changes of the current database session"""
        self.__session.commit()

    def delete(self, obj=None):
        """delete from the current database session obj if not None"""
        if obj is not None:
            self.__session.delete(obj)

    def close(self):
        """call remove() method on the private session attribute"""
        self.__session.remove()

    def reload(self):
        """create all tables in the database"""
        Base.metadata.create_all(self.__engine)
        session_factory = sessionmaker(
            bind=self.__engine, expire_on_commit=False
        )
        Session = scoped_session(session_factory)
        self.__session = Session

    def get(self, cls, id):
        """returns the object based on the class name and id"""
        if cls and id:
            key_name = "{}.{}".format(cls.__name__, id)
            return self.all(cls).get(key_name)
        return None

    def count(self, cls=None):
        """counts the number of objects in fle storage"""
        if cls:
            return len(self.all(cls))
        else:
            return len(self.all())
