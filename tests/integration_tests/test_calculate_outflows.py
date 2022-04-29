import unittest

from python_module import python_module



class TestPythonModule(unittest.TestCase):
    """Example test"""


    def test_calculate_OutFlow(self):
        sub_catchment = python_module.sub_catchment(catchment_id='110')
        response = sub_catchment.calculate_OutFlow(catchment_id='110',product_id='372',start_date = "2012-12-09",end_date = "2013-03-11",plot=False)

        self.assertIsNotNone(response)
        self.assertEqual(type(response), dict)
        #self.assertEqual(response['115']['Precipitation cm']['0'],0.2590594454)  

if __name__ == '__main__':
    unittest.main()