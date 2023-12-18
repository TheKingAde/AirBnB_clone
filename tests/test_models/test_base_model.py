#!/usr/bin/python3
"""Test script for the BaseModel class"""
import unittest
from models.base_model import BaseModel
from datetime import datetime
import json
import os
from models import storage


class TestBaseModel(unittest.TestCase):
    """Test cases for the BaseModel class"""

    def setUp(self):
        """Set up the test environ before each test"""
        self.model = BaseModel()
        self.model_id = self.model.id

    def tearDown(self):
        """clean up test environ after eac test"""
        if os.path.exists("file.json"):
            os.remove("file.json")

    def test_instance_creation(self):
        """Tests BaseModel instance creation"""
        self.assertIsInstance(self.model, BaseModel)
        self.assertTrue(hasattr(self.model, 'id'))
        self.assertTrue(hasattr(self.model, 'created_at'))
        self.assertTrue(hasattr(self.model, 'updated_at'))
        self.assertIsInstance(self.model.id, str)
        self.assertIsInstance(self.model.created_at, datetime)
        self.assertIsInstance(self.model.updated_at, datetime)

    def test_save_method(self):
        """Test save Method of the BaseModel"""
        initial_updated_at = self.model.updated_at
        self.model.save()
        self.assertNotEqual(initial_updated_at, self.model.updated_at)

    def test_to_dict_method(self):
        """Test the to_dict method"""
        obj_dict = self.model.to_dict()
        self.assertIsInstance(obj_dict, dict)
        self.assertIn('__class__', obj_dict)
        self.assertIn('created_at', obj_dict)
        self.assertIn('updated_at', obj_dict)
        self.assertEqual(obj_dict['__class__'], 'BaseModel')
        self.assertEqual(
                obj_dict['created_at'],
                self.model.created_at.isoformat()
                )
        self.assertEqual(
                obj_dict['updated_at'],
                self.model.updated_at.isoformat()
                )

    def test_str_method(self):
        """Test the string method"""
        obj_str = str(self.model)
        self.assertIsInstance(obj_str, str)
        self.assertIn('BaseModel', obj_str)
        self.assertIn(self.model.id, obj_str)
        self.assertIn(str(self.model.__dict__), obj_str)

    def test_save_and_reload(self):
        """Test saving and reloading"""
        self.model.save()
        new_model = BaseModel()
        storage.reload()
        self.assertIn('BaseModel.' + new_model.id, storage.all())

    def test_save_to_file_and_reload(self):
        """test save to file and reloading"""
        self.model.save()
        new_model = BaseModel()
        self.model.save()
        storage.reload()
        self.assertIn('BaseModel.' + new_model.id, storage.all())

    def test_save_and_reload_with_file_path(self):
        """test saving and reloading with specified file path"""
        self.model.save()
        new_model = BaseModel()
        storage.reload(file_path="file.json")
        self.assertIn('BaseModel.' + new_model.id, storage.all())
        self.assertIn('BaseModel.' + self.model.id, storage.all())

    def test_save_to_file_and_reload_with_file_path(self):
        """test saving to file and reloading"""
        self.model.save()
        new_model = BaseModel()
        self.model.save()
        storage.reload("file.json")
        self.assertIn('BaseModel.' + new_model.id, storage.all())
        self.assertIn('BaseModel.' + self.model.id, storage.all())

    def test_create_instance_with_dict(self):
        """test creating a BaseModel Instance from a dcitionary"""
        obj_dict = self.model.to_dict()
        new_model = BaseModel(**obj_dict)
        self.assertEqual(self.model.id, new_model.id)
        self.assertEqual(self.model.created_at, new_model.created_at)
        self.assertEqual(self.model.updated_at, new_model.updated_at)


if __name__ == '__main__':
    unittest.main()
