import unittest
from models.base_model import BaseModel


class TestBaseModel(unittest.TestCase):
    """Test cases for the BaseModel class."""

    def test_str_representation(self):
        model = BaseModel(my_number=42, name='Test Model')
        expected_str = (
            "[BaseModel] ({}) {{'my_number': 42, 'name': 'Test Model', "
            "'updated_at': {!r}, 'id': {!r}, 'created_at': {!r}}}"
        ).format(model.id, model.updated_at, model.id, model.created_at)
        self.assertEqual(str(model), expected_str)

    def test_save_method(self):
        model = BaseModel()
        initial_updated_at = model.updated_at
        model.save()
        self.assertNotEqual(initial_updated_at, model.updated_at)

    def test_to_dict_method(self):
        model = BaseModel(my_number=42, name='Test Model')
        model_dict = model.to_dict()

        expected_dict = {
            'my_number': 42,
            'name': 'Test Model',
            '__class__': 'BaseModel',
            'updated_at': model.updated_at.isoformat(),
            'id': model.id,
            'created_at': model.created_at.isoformat()
        }

        self.assertEqual(model_dict, expected_dict)


if __name__ == '__main__':
    unittest.main()
