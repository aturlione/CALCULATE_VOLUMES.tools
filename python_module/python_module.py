# -*- coding: utf-8 -*-
"""
Created on Mon Apr 25 12:10:54 2022

@author: Anabela Turlione
"""

import requests
import json
import pandas as pd
import matplotlib.pyplot as plt
from datetime import  datetime
import time


class sub_catchment:
    
    """
    Defines a sub-ctachment with all its metods
    """
    
    def __init__(self,catchment_id):
        self.catchment_id = catchment_id
        
    #Funcion para obtener los datos de los diferentes métodos que hay en la API 
    def obtain_data(self,section,param=None):    

        url = 'https://apisatd-katari.ihcantabria.com/v1/public/'+section

        headers = {'Accept':  'application/json'}

        r1 = requests.get(url, headers=headers) 
        data1=json.loads(r1.text)
        if param:
            r1 = requests.get(url, headers=headers,  json =param) 
            data1=json.loads(r1.text)
        return data1
#------------------------------------------------------------------------------------------------------------------------    
    #Método hydrobid: 
    #Aplico el modelo hydrobid a una cuenca dada en un rango de fechas dado
#------------------------------------------------------------------------------------------------------------------------        
    
    def hydrobid(self,catchment_id,product_id,start_date,end_date):
        print('Calculating hydrobid on sub-catchtment {} ...'.format(catchment_id))
        #inicio = time.time()

        #obtengo la sub-catchment
        sub_catchments_hydrobid = self.obtain_data('hydrographies/sub-catchments-hydrobid/'+catchment_id+'/geo-json')


        #obtengo los datos de la catchment particular con el id
        comid = sub_catchments_hydrobid['features'][0]['properties']['comid']


        #Ataco en ApiProcess el método Hydrobid
        url = "https://apiprocess.ihcantabria.com/satd-katari-geoprocesses/SATD-KATARI ApiProcess/Hydrobid"
        #headers = {'Accept':  'application/json'}

        param = {
          "product_id": product_id,
          "comid": int(comid),
          "start_date": start_date,
          "end_date": end_date,
          "min_lat": 0.,
          "max_lat": 0.,
          "min_lon": 0.,
          "max_lon": 0.
        }    

        post_np=requests.post(url,  json =param) 

        result=json.loads(post_np.text)
        result=json.loads(result['daily'])
        #result_pd=pd.DataFrame(result)


        #fin = time.time()
        #print('time  {} s'.format(fin-inicio))

        return result
    
#------------------------------------------------------------------------------------------------------------------------        
    # Método calculate_OutFlow:
    
    # Dado el id de una cuenca, fecha de inicio y fecha de fin, encuentro todas las upper-catchments 
    #y calculo el outflow para cada una usando hydrobid
#------------------------------------------------------------------------------------------------------------------------        
    def calculate_OutFlow(self,catchment_id,product_id,start_date,end_date,plot=False):

        #obtengo todas las "upper-sub-catchments" correspondientes
        section = 'hydrographies/sub-catchments-hydrobid/'+catchment_id+'/upper-sub-catchments-hydrobid/geo-json'

        uppers = self.obtain_data(section)

        #obtengo los parámetros de cada "upper-sub-catchment" para usar en hydrobid
        idss=[]
        #comids=[]
        results={}

        for i in range(1,len(uppers['features'])):

            #ids y comids
            #comids = int(uppers['features'][i]['properties']['comid'])
            ids = uppers['features'][i]['properties']['id']

            idss.append(ids)

            #Ataco en ApiProcess el método Hydrobid para obtener el caudal m3/s de cada una de las cuencas en un período de tiempo.
            results[str(ids)]=self.hydrobid(str(ids),product_id,start_date,end_date)

        #plot caudales    
        if plot:
            import matplotlib.dates as mdates
            fig,ax = plt.subplots()

            for i in range(0,len(idss)):
                x=pd.DataFrame(results[str(idss[i])]).iloc[:,1]
                y=pd.DataFrame(results[str(idss[i])]).iloc[:,2]
                plt.plot(x,y)

                ax.xaxis.set_tick_params(reset=True)
                ax.xaxis.set_major_locator(mdates.MonthLocator(interval=1))
                plt.xticks(rotation='vertical')
                plt.ylabel('Modeled Outflow m3/s')
                plt.title('Caudales entrantes para la cuenca {}'.format(catchment_id))

            plt.legend(idss)

        return results
#------------------------------------------------------------------------------------------------------------------------        
    #Método calculate_total_volumes:
    
    #caculate total volume using results from "calculate_Outflows"
#------------------------------------------------------------------------------------------------------------------------        
    
    def calculate_total_volumes(self,results):
        print('Calculate entering volumes ...')
        #inicio_time = time.time()

        Seassonal_volume = {}

        for sub_catchment in results.keys():
            Outflows = pd.DataFrame(results[sub_catchment])['Modeled Outflow m3/s']

            dates = pd.DataFrame(results[sub_catchment]).iloc[:,1]

            Seassonal_Outflows = {'spring':[],'summer':[],'winter':[],'autumn':[]}

            Seassonal_volume[sub_catchment] = {'spring':[],'summer':[],'winter':[],'autumn':[]}

            for i in range(0,len(dates)):
                date = datetime.strptime(dates[i],'%Y-%m-%d')
                Outflow = Outflows[i]
                year = date.year

                seassons = [('summer', datetime(year,  1,  1),  datetime(year,  3, 20)), 
                  ('autumn', datetime(year,  3, 21),  datetime(year, 6, 20)),
                  ('winter', datetime(year, 6, 21),  datetime(year, 9, 20)),
                  ('spring', datetime(year,  9, 21),  datetime(year,  12, 21)),
                  ('summer', datetime(year,  12, 21),  datetime(year,  12, 31))             
                  ]

                #Asigno estación a la fecha
                for estacion, inicio, fin in seassons:
                    if inicio <= date <= fin:
                        seasson = estacion

                Seassonal_Outflows[seasson].append(Outflow)

            for seasson in ['spring','summer','winter','autumn']:
                #Integro en el tiempo para encontrar el volumen total entrante en m3 para cada "upper subcatchment". 
                #Método de Euler con paso= 1 día (86400 s)
                Seassonal_volume[sub_catchment][seasson]= sum(Seassonal_Outflows[seasson]*86400)

            Seassonal_volume[sub_catchment]['annual'] = sum([Seassonal_volume[sub_catchment][seasson] for seasson in ['spring','summer','winter','autumn']])

        #fin = time.time()

        #print('time  {} s'.format(fin-inicio_time))    
        return Seassonal_volume
#------------------------------------------------------------------------------------------------------------------------    
    #Método obtain_water_demands:
    
    #Calculate water demands
#------------------------------------------------------------------------------------------------------------------------
    #param = {
    #          "sub-catchment-hydrobid-id": int,
    #          "lon-min": float,
    #          "lat-min": float,
    #          "lon-max": float
    #          "lat-max": float
    #        }

    def obtain_water_demands(self,param,demand_kind):
        print('Calculating {} ...'.format(demand_kind))
        #inicio = time.time()

        subcatcment_id = str(param["sub-catchment-hydrobid-id"])
        #obtengo las demandas

        #mining-centers usa un formato diferente para el url
        if demand_kind == 'mining-centers':

            section = 'socioeconomics/mining-centers'+ \
            '?sub-catchment-hydrobid-id=' + subcatcment_id + \
            '&lon-min=' + str(param['lon-min']) + \
            '&lat-min=' + str(param['lat-min']) + \
            '&lon-max=' + str(param['lon-max']) + \
            '&lat-max=' + str(param['lat-max'])

            water_demands = self.obtain_data(section,param)

            return water_demands
        # potable-water-demands, irrigations y ecosystems usan el mismo formato
        else:

            water_demands = self.obtain_data('hydrographies/'+demand_kind,param)

            water_summer = []
            water_winter = []
            water_autumn = []
            water_spring = []
            water_annual = []

            for i in range(0,len(water_demands)):

                water_winter.append(water_demands[i]['winterDemand'])

                water_summer.append(water_demands[i]['summerDemand'])

                water_autumn.append(water_demands[i]['autumnDemand'])

                water_spring.append(water_demands[i]['springDemand'])

                water_annual.append(water_demands[i]['annualDemand'])


            total_winter = sum(water_winter)
            total_summer = sum(water_summer)
            total_autumn = sum(water_autumn)
            total_spring = sum(water_spring)

            total_annual = sum(water_annual)

            #fin = time.time()

            #print('time  {} s'.format(fin-inicio)) 
            return {'winter' : total_winter, 'summer': total_summer, 'autumn' : total_autumn, 'spring' : total_spring, 'annual': total_annual}
#------------------------------------------------------------------------------------------------------------------------
    #Método calculate_resultant_volume:
    
    #Resultado final, volumen entrante - volumen saliente
#------------------------------------------------------------------------------------------------------------------------
    def calculate_resultant_volume(self,catchment_id,product_id,start_date,end_date, custom_demands=None):
        inicio = time.time()
    
        #calculo las demandas
        param = {
              "sub-catchment-hydrobid-id": int(catchment_id),
              "lon-min": 0.,
              "lat-min": 0.,
              "lon-max": 0.,
              "lat-max": 0.
            }

        #Calculo la demanda de Agua Potable
        potable_water_demands = self.obtain_water_demands(param,'potable-water-demands')

        #Calculo la demanda de Riego
        irrigations = self.obtain_water_demands(param,'irrigations')

        #Calculo la demanda de Act. Industriales
        mining_centers = self.obtain_water_demands(param,'mining-centers')

        #Calculo la demanda de Ecosistémico
        ecosystems = self.obtain_water_demands(param,'ecosystems')

        demands = {'potable-water-demands':potable_water_demands,
                    'irrigations':irrigations,
                    'mining-centers':mining_centers,
                    'ecosystems':ecosystems, 
    }

        if custom_demands:
            for demand in custom_demands.keys():
                for seasson in custom_demands[demand].keys():
                    demands[demand][seasson] = custom_demands[demand][seasson]*demands[demand][seasson]

        #Obtengo los caudales entrantes con hydrobid
        results=self.calculate_OutFlow(catchment_id,product_id,start_date,end_date)

        #Calculo los volumenes totales entrantes por upper-sub-catchment y estación
        total_upper_volumes = self.calculate_total_volumes(results)  
        
        seassons = ['spring','summer','winter','autumn','annual']

        total_volumes = {}
        total_demand = {}
        final_result = {}

        for seasson in seassons:
            #Volumen entrante total
            total_volumes[seasson] = 0
            for sub_catchment in total_upper_volumes.keys():
                total_volumes[seasson] += total_upper_volumes[sub_catchment][seasson]

            #demanda total
            total_demand[seasson] = demands['potable-water-demands'][seasson]+demands['ecosystems'][seasson]+demands['irrigations'][seasson]

            final_result[seasson] = total_volumes[seasson]-total_demand[seasson]
        
        #calculo la navegación
        navigation_section = 'hydrographies/sub-catchments-hydrobid/'+catchment_id+'/sub-catchment-hydrobid-navigations'
        navigation = self.obtain_data(navigation_section,param=None)
        
        output_results = {'upper entering vols': total_upper_volumes,'total entering vol':total_volumes, 'total demands':total_demand,'final result':final_result,
                'navigation' : navigation}

        fin = time.time()

        print('total time ',fin-inicio)
        
        
        return json.dumps(output_results)
    

if __name__ == "__main___":
    sub_catchment