#!/usr/bin/python3

import uuid
from datetime import datetime
from collections import OrderedDict


class BaseModel:
    """A base class for all other classes"""

    def __init__(self, my_number=None, name=None, *args, **kwargs):
        """initialize a new instance of BaseModel"""
        self.id = str(uuid.uuid4())
        self.created_at = datetime.now()
        self.updated_at = self.created_at
        self.my_number = my_number
        self.name = name
        if kwargs:
            for key, value in kwargs.items():
                if key == "created_at" or key == "updated_at":
                    value = datetime.strptime(value, "%Y-%m-%dT%H:%M:%S.%f")
                    setattr(self, key, value)

    def __str__(self):
        """Return a string representation of the instance"""
        O_A = ["my_number", "name", "updated_at", "id", "created_at"]
        # O_A stands for ordered attribute
        attributes_str = ", ".join(
                "'{}': {!r}".format(attr, getattr(self, attr)) for attr in O_A
        )
        return "[{}] ({}) {{{}}}".format(self.__class__.__name__, self.id,
                                         attributes_str)

    def save(self):
        """Update the updated_at attribute with the current datetime"""
        self.updated_at = datetime.now()

    def to_dict(self):
        """Return a dict representation of the instance with ordered keys"""
        ordered_keys = [
            "my_number", "name", "__class__", "updated_at", "id", "created_at"
        ]
        result = {
            key: getattr(self, key)
            for key in ordered_keys if hasattr(self, key)
        }

        result['__class__'] = self.__class__.__name__

        for key, value in result.items():
            if isinstance(value, datetime):
                result[key] = value.isoformat()

        return result
