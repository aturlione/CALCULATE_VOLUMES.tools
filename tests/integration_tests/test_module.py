import unittest

from python_module import python_module


class TestPythonModule(unittest.TestCase):
    """Example test"""

    def test_python_module(self,catchment_id):
        response = python_module.sub_catchment(catchment_id)
        self.assertIsNotNone(response)
        self.assertEqual(type(response), dict)
