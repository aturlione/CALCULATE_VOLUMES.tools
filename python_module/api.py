# -*- coding: utf-8 -*-
"""
Created on Tue Apr 26 14:47:46 2022

@author: Anabela Turlione
"""
from flask import Flask, jsonify
from python_module import sub_catchment


app = Flask(__name__)

@app.route("/<catchment_id>")
def api_calculate_volume( product_id = '372',catchment_id = '110',start_date = "2012-12-09",end_date = "2013-03-11",custom_demands=None):
    try:
        # "custom_demand" are optional parameters that allow the user to define customs percentages for each demand in a given sub-catchment. 
        # Eg: ustom_demands={'potable-water-demands':{'summer':0.5}}    
        
        #creo la subcatchment   
        sub_catch = sub_catchment(catchment_id)
        
        # Resultados -- Archivo json que contiene la siguiente información: 
        Results = sub_catch.calculate_resultant_volume(product_id,start_date,end_date,custom_demands = custom_demands)
        
        return jsonify(Results)
    except Exception as ex:
        return "Error"

if __name__=='__main__':
    app.run(debug=True)
    
   