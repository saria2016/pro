#!/usr/bin/env python3
"""model for blue print view"""
from flask import Blueprint, make_response, jsonify, abort
from models import storage
from models.user import User
from models.task import Task
import bcrypt

app_views = Blueprint("app_views", __name__, url_prefix="/api/v1")


def get_match(cls, id):
    """GET: get the object of a specific class based on its id"""
    obj = storage.get(cls, id)
    if obj:
        return jsonify(obj.to_dict())
    abort(404)


def delete_match(cls, id):
    """DELETE: delete the object of a specific class based on its id"""
    obj = storage.get(cls, id)
    if obj:
        storage.delete(obj)
        storage.save()
        return make_response(jsonify({}), 200)
    abort(404)


def register_new(p_cls, ch_cls, p_id, kwargs):
    """POST: creating a new object for the class"""
    if p_cls == User and ch_cls is None:
        # validate if the current content exists
        all_obj = storage.all(p_cls).values()
        for obj in all_obj:
            if obj.email == kwargs["email"]:
                abort(409, description="Object instance already exists")
        if "password" in kwargs:
          password = kwargs["password"]
          hash_pswd = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
          kwargs["password"] = hash_pswd
        obj = p_cls(**kwargs)
        obj.save()
        return get_match(p_cls, obj.id)
    else:
        abort(404)

    # if p_cls == User and ch_cls == Task:
    #     # validate if the task object already exists
    #     # all_obj = storage.all(ch_cls).values()
    #     # for obj in all_obj:
    #     #     if obj.model_name == kwargs["model_name"]:
    #     #         abort(409, description="Object instance already exists")        
    #     # kwargs["brand_id"] = p_id
    #     # obj = ch_cls(**kwargs)
    #     # obj.save()
    #     # return jsonify(obj.to_dict()), 201
    #     pass
    # else:
    #     abort(404)
    

def update_match(obj, kwargs):
    """PUT: update the brand object"""
    if "password" in kwargs:
      password = kwargs["password"]
      hash_pwsd = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
      kwargs["password"] = hash_pwsd
    for key, value in kwargs.items():
      setattr(obj, key, value)   
    obj.save()
    ret_data = jsonify(obj.to_dict())
    return make_response(ret_data, 200)
  
  
def validate_user(p_cls, kwargs):
    """POST: validate the user credentials"""
    if "email" not in kwargs:
        abort(400, description="Error: Missing email")        
    if "password" not in kwargs:
        abort(400, description="Error: Missing password")
    # validate if the current content exists
    all_obj_users = storage.all(p_cls).values()
    # validate if the email exists
    email = kwargs["email"]
    for obj in all_obj_users:
        if obj.email == email:
            # validate the password
            if bcrypt.checkpw(kwargs["password"].encode('utf-8'), obj.password.encode('utf-8')):            
                # password is valid
                return jsonify ({"login": "Successful", "id": obj.id}), 201
            else:
                # password is invalid
                abort(401, description="Password Incorrect")
        else:
          continue
    else:
      abort(401, description="Invalid email")


# used to instantiate the blueprint routes upon program start-up
from api.v1.views.users import *
from api.v1.views.tasks import *

