import unittest

from python_module import python_module

print('enter catchment_id:')
catchment_id = input()

print('enter start_date (yyyy-mm-dd):')
start_date = input()

print('enter end_date (yyyy-mm-dd):')
end_date = input()

print(type(catchment_id))
class TestPythonModule(unittest.TestCase):
    """Example test"""

    def test_hydrobid(self):
        sub_catchment = python_module.sub_catchment(catchment_id)
        response = sub_catchment.hydrobid(catchment_id,'372',start_date,end_date)
        
        self.assertIsNotNone(response)
        self.assertEqual(type(response), dict)



if __name__ == '__main__':
    unittest.main()