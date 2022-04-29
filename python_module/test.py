from python_module import *

subcatchment=sub_catchment(110)

        
sub_catchment = sub_catchment(catchment_id='110')
response = sub_catchment.calculate_resultant_volume(product_id = '372',start_date = "2012-12-09",end_date = "2013-03-11",custom_demands=None)
print(response)

    