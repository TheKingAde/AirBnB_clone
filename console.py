#!/usr/bin/env python3

import cmd
import shlex
from models import storage
from models.base_model import BaseModel


class HBNBCommand(cmd.Cmd):
  prompt = '(hbnb) '
  __classes = {"BaseModel"}

  def do_quit(self, arg):
    """Quit command to exit the program"""
    return True

  def do_EOF(self, arg):
    """Quit command to exit the program"""
    return True

  def do_create(self, arg):
    """Creates a new instance of BaseModel"""
    args = shlex.split(arg)
    if len(args) < 1:
      print("** class name missing **")
      return
    class_name = args[0]
    if class_name not in self.__classes:
      print("** class doesn't exist **")
      return
    from models.base_model import BaseModel
    if len(args) > 1:
      instance_args = ' '.join(args[1:])
      try:
        new_instance = eval(class_name + "(" + instance_args + ")")
        new_instance.save()
        print(new_instance.id)
      except Exception as e:
        print(e)
    else:
      new_instance = BaseModel()
      new_instance.save()
      print(new_instance.id)

  def do_show(self, arg):
    """Prints the string representation of an instance based on the class name and id"""
    try:
      if not arg:
        raise SyntaxError("** class name missing **")
      args = arg.split(" ")
      class_name = args[0]
      if class_name not in self.__classes:
        raise NameError("** class doesn't exist **")
      obj_id = args[1] if len(args) >= 2 else None
      if obj_id is None:
        raise IndexError("** instance id missing **")
      obj_dict = storage.all()
      key = "{}.{}".format(class_name, obj_id)
      if key in obj_dict:
        print(obj_dict[key])
      else:
        raise KeyError("** no instance found **")
    except (SyntaxError, NameError, IndexError, KeyError) as e:
      print(e)
      
  def do_destroy(self, arg):
    """Deletes an instance (save the change to JSON file)"""
    try:
      if not arg:
        raise SyntaxError("** class name missing **")

      args = arg.split(" ")
      class_name = args[0]

      if class_name not in self.__classes:
        raise IndexError("** class doesn't exist **")
        
      obj_id = args[1] if len(args) >= 2 else None
      if obj_id is None:
        raise IndexError("** instance id missing **")
      key = "{}.{}".format(class_name, obj_id)
      obj_dict = storage.all()

      if key in obj_dict:
        del obj_dict[key]
        storage.save()
      else:
        raise KeyError("** no instance found **")

    except (SyntaxError, IndexError, KeyError) as e:
            print(e)


  def do_all(self, arg):
    """Prints all string representation of all instances"""
    try:
        if not arg:
            raise SyntaxError("** class name missing **")

        class_name = arg.split(" ")[0]

        if class_name not in self.__classes:
            raise NameError("** class doesn't exist **")

        obj_dict = storage.all()
        instances = [
          str(obj_dict[key])
          for key in obj_dict 
          if key.startswith(class_name + ".")]

        if instances:
            print(instances)
        else:
            print("** no instances found **")

    except (SyntaxError, NameError) as e:
        print(e)

  def do_update(self, arg):
    """Updates an instance based on the class name and id by adding or updating attr"""
    try:
        if not arg:
            raise SyntaxError("** class name missing **")

        args = arg.split(" ")
        class_name = args[0]

        if class_name not in self.__classes:
            raise IndexError("** class doesn't exist **")

        if len(args) < 2:
            raise IndexError("** instance id missing **")

        obj_id = args[1]
        key = "{}.{}".format(class_name, obj_id)
        obj_dict = storage.all()

        if key not in obj_dict:
            raise KeyError("** no instance found **")

        if len(args) < 3:
            raise IndexError("** attribute name missing **")

        if len(args) < 4:
            raise IndexError("** value missing **")

        obj = obj_dict[key]
        attribute_name = args[2]
        attribute_value = args[3]

        if attribute_name in obj.__dict__:
            # Perform conversion to the attribute type (string, integer, or float)
            if isinstance(obj.__dict__[attribute_name], str):
                obj.__dict__[attribute_name] = str(attribute_value)
            elif isinstance(obj.__dict__[attribute_name], int):
                obj.__dict__[attribute_name] = int(attribute_value)
            elif isinstance(obj.__dict__[attribute_name], float):
                obj.__dict__[attribute_name] = float(attribute_value)

            obj.save()
        else:
            print("** attribute name not found **")

    except (SyntaxError, IndexError, KeyError) as e:
        print(e)



if __name__ == '__main__':
  HBNBCommand().cmdloop()

