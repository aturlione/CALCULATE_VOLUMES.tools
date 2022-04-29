import unittest

from python_module import python_module



class TestPythonModule(unittest.TestCase):
    """Example test"""

    def test_obtain_potable_water_demands(self):
        
        sub_catchment = python_module.sub_catchment('110')
        response = sub_catchment.obtain_water_demands('110',demand_kind='irrigations')

       

        self.assertIsNotNone(response)
        self.assertEqual(type(response), dict)
        
        


if __name__ == '__main__':
    unittest.main()