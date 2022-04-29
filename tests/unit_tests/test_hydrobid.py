import unittest

from python_module import python_module



class TestPythonModule(unittest.TestCase):
    """Example test"""

    def test_hydrobid(self):
        sub_catchment = python_module.sub_catchment(catchment_id='110')
        response = sub_catchment.hydrobid(catchment_id='110',product_id='372',start_date = "2012-12-09",end_date = "2013-03-11")

        self.assertEqual(response['Modeled Outflow m3/s']['42'],0.0490592048)  


if __name__ == '__main__':
    unittest.main()