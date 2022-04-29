import unittest

from python_module import python_module



class TestPythonModule(unittest.TestCase):
    """Example test"""

    def test_obtain_data(self):
        
        sub_catchment = python_module.sub_catchment(catchment_id='110')
        response = sub_catchment.obtain_data('hydrographies/sub-catchments-hydrobid/110')
        
        
        self.assertIsNotNone(response)
        self.assertEqual(type(response), dict)
        


if __name__ == '__main__':
    unittest.main()