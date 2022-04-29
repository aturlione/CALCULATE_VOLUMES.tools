import unittest

from python_module import python_module



class TestPythonModule(unittest.TestCase):
    """Example test"""

    def test_hydrobid(self):
        
        sub_catchment = python_module.sub_catchment(catchment_id='110')
        results = sub_catchment.calculate_OutFlow(catchment_id='110',product_id='372',start_date = "2012-12-09",end_date = "2013-03-11",plot=False)
        response = sub_catchment.calculate_total_volumes(results)

        
        self.assertIsNotNone(response)
        self.assertEqual(type(response), dict)          
        self.assertEqual([response['115']['summer'],response['116']['summer'],response['117']['summer'],response['118']['summer']], [2535038.9923901334,1458562.1746350361,566308.6677827392,602866.7538935213])    

if __name__ == '__main__':
    unittest.main()