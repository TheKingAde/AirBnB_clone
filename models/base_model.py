#!/usr/bin/python3

import uuid
from datetime import datetime
from models import storage


class BaseModel:
  """A base class for all other classes"""

  def __init__(self, *args, **kwargs):
    """initialize a new instance of BaseModel"""
    self.id = str(uuid.uuid4())
    if kwargs:
      for key, value in kwargs.items():
        if key == "created_at" or key == "updated_at":
          value = datetime.strptime(value, "%Y-%m-%dT%H:%M:%S.%f")
          setattr(self, key, value)
    else:
      self.created_at = datetime.now()
      self.updated_at = self.created_at
      storage.new(self)

  def __str__(self):
    """Return a string representation of the instance"""
    return "[{}] ({}) {}".format(self.__class__.__name__, self.id,
                                 self.__dict__)

  def save(self):
    """Update the updated_at attribute with the current datetime"""
    self.updated_at = datetime.now()
    storage.save()

  def to_dict(self):
    """Return a dict representation of the instance with ordered keys"""
    obj_dict = self.__dict__.copy()
    obj_dict['__class__'] = self.__class__.__name__
    obj_dict['created_at'] = self.created_at.isoformat()
    obj_dict['updated_at'] = self.updated_at.isoformat()
    return obj_dict
