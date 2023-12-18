#!/usr/bin/python3
"""BaseModel Module Class"""
import uuid
from datetime import datetime
from models import storage


class BaseModel:
    """Defines the BaseModel Class."""

    def __init__(self, *args, **kwargs):
        """Initialize new BaseModel

        Args:
            *args: unusued
            *kwargs: key/value pair (dict)
        """
        if not kwargs:
            self.id = str(uuid.uuid4())
            self.created_at = self.updated_at = datetime.now()
            storage.new(self)
        else:
            for key, value in kwargs.items():
                if key == '__class__':
                    continue
                if key in ('created_at', 'updated_at'):
                    value = datetime.strptime(value, '%Y-%m-%dT%H:%M:%S.%f')
                setattr(self, key, value)
            if 'id' not in kwargs:
                self.id = str(uuid.uuid4())
            if 'created_at' not in kwargs:
                self.created_at = datetime.now()
            if 'updated_at' not in kwargs:
                self.updated_at = datetime.now()

        if ('id' not in kwargs or
                'created_at' not in kwargs or
                'updated_at' not in kwargs):
            storage.new(self)

    def __str__(self):
        """Return a string representation of the instance"""
        return "[{}] ({}) {}".format(self.__class__.__name__, self.id,
                                     self.__dict__)

    def save(self):
        """Update the updated_at attribute with the current datetime"""
        self.updated_at = datetime.now()
        storage.new(self)
        storage.save()

    def to_dict(self):
        """Return a dict representation of the instance with ordered keys"""
        obj_dict = self.__dict__.copy()
        class_name = self.__class__.__name__
        obj_dict['__class__'] = class_name
        obj_dict['created_at'] = self.created_at.isoformat()
        obj_dict['updated_at'] = self.updated_at.isoformat()
        obj_dict['id'] = self.id
        return obj_dict
