from python_module import *

subcatchment=sub_catchment(110)

#results=subcatchment.calculate_resultant_volume('110','372',start_date = "2012-12-09",end_date = "2013-03-11")
#print(results)





section = 'hydrographies/potable-water-demands/geo-json?'+'sub-catchment-hydrobid-id='+ '110'  
                 

results=subcatchment.obtain_data(section)

print(results)
#sub_cathments=subcatchment.obtain_data('hydrographies/sub-catchments-hydrobid')



#ids=[sub_cathments[i]['id'] for i in range(0,len(sub_cathments))]


#print(ids)

# for i in ids:
#     sub_catch = sub_catchment(i)
#     section = 'hydrographies/potable-water-demands?'+'sub-catchment-hydrobid-id='+ str(i)  \
#                 + '&lon-min=0&lat-min=0&lon-max=0&lat-max=0'

#     results=sub_catch.obtain_data(section)
#     print('sub-catchment-id:',i,results,'\n')
    