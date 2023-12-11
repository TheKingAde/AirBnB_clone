#!/usr/bin/python3

import json


class FileStorage:
  __file_path = "file.json"
  __objects = {}

  def all(self):
    return self.__objects

  def new(self, obj):
    key = "{}.{}".format(obj.__class__.__name__, obj.id)
    self.__objects[key] = obj

  def save(self):
    with open(self.__file_path, 'w') as f:
      obj_dict = {key: obj.to_dict() for key, obj in self.__objects.items()}
      json.dump(obj_dict, f)

  def reload(self):
    try:
      with open(self.__file_path, 'r') as f:
        obj_dict = json.load(f)
        from models.base_model import BaseModel
        from models.user import User
        classes = {
                "BaseModel": BaseModel,
                "User": User,
                "Place": Place,
                "State": State,
                "City": City,
                "Amenity": Amenity,
                "Review": Review
            }
        for key, value in obj_dict.items():
          class_name, obj_id = key.split(".")
          obj_class = classes[class_name]
          obj = obj_class(**value)
          self.__objects[key] = obj
    except FileNotFoundError:
      pass
  
  def classes(self):
      """Implement a method to return the available classes"""
      return self.__objects.keys()
