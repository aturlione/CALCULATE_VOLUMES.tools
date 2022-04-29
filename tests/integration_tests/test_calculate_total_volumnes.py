import unittest

from python_module import python_module



class TestPythonModule(unittest.TestCase):
    """Example test"""

    def test_calculate_total_volumns(self):
        
        sub_catchment = python_module.sub_catchment(catchment_id='110')
        results = sub_catchment.calculate_OutFlow(catchment_id='110',product_id='372',start_date = "2012-12-09",end_date = "2013-03-11",plot=False)
        response = sub_catchment.calculate_total_volumes(results)

        
        self.assertIsNotNone(response)
        self.assertEqual(type(response), dict)
        


if __name__ == '__main__':
    unittest.main()