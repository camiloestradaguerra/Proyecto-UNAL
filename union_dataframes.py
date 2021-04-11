#!/usr/bin/env python
# coding: utf-8

# In[2]:


from shapely import wkt
import pandas as pd
import geopandas as gpd
import numpy as np
import math


import timeit

# Import necessary geometric objects from shapely module

from shapely.geometry import Point, LineString, Polygon
from shapely.geometry import MultiPoint, MultiLineString, MultiPolygon, box
import fiona
from pyproj import Proj  # to project the values of Point
nys = Proj(init='EPSG:3857') 



dataframe1 = pd.read_csv('merged_nuse1.csv')
dataframe1 = gpd.GeoDataFrame(dataframe1, geometry=gpd.points_from_xy(dataframe1.LONGITUD, dataframe1.LATITUD),crs="EPSG:3857")

start = timeit.default_timer()
######################################################################

##########################################################
####### ORGANIZACION DEL DATAFRAME MERGED_NUSE1.CSV #######
##########################################################
dataframe1['FECHA'] = pd.to_datetime(dataframe1['FECHA'])
dataframe1_enero_18 = dataframe1[(dataframe1['FECHA'] >= '2018-01-01 00:00:00') & (dataframe1['FECHA'] <= '2018-01-31 23:59:59')].sort_values(["FECHA"])
dataframe1_enero_18['FECHA'] = dataframe1_enero_18['FECHA'].astype(str)
dataframe1_enero_18 = dataframe1_enero_18.sort_values(["FECHA"]) 
data_df1_enero_18 = gpd.GeoDataFrame(dataframe1_enero_18, columns=['LONGITUD', 'LATITUD', 'FECHA','geometry'])
data_df1_enero_18['cov1'] = " "
data_df1_enero_18['cov2'] = " "
data_df1_enero_18['cell'] = " "
data_df1_enero_18 = data_df1_enero_18.to_crs("EPSG:3857")

for i in range(0, len(data_df1_enero_18)):
    data_df1_enero_18['geometry'].iloc[i] = Point(nys(data_df1_enero_18['geometry'].iloc[i].x, data_df1_enero_18['geometry'].iloc[i].y))
 
data_df1_enero_18 = data_df1_enero_18[(data_df1_enero_18['FECHA'] >= '2018-01-01 00:00:00') & (data_df1_enero_18['FECHA'] <= '2018-01-31 23:59:59')]    

#data_df1_enero_18 = data_df1_enero_18.iloc[0:3000,:]

###########################################################################################
stop = timeit.default_timer()
execution_time = stop - start
print("1ra Parte: Program Executed in "+str(execution_time)) # It returns time in seconds        


start = timeit.default_timer()
######################################################################

###########################################
####### UNION DE LOS DOS DATAFRAMES #######
###########################################

# Importamos el dataframe poligonos.csv
covs_df = pd.read_csv('poligonos_df_final.csv')
covs_df = gpd.GeoDataFrame(covs_df, columns=['geometry','Núm de Comando de Atención Inmediata 2020','Rest y Bares'])
covs_df = covs_df.rename(columns={'Rest y Bares' : 'cov1', 'Núm de Comando de Atención Inmediata 2020' : 'cov2'})
# Normalizamos las columnas de covariados
covs_df['cov1'] = covs_df['cov1']/covs_df['cov1'].sum()
covs_df['cov2'] = covs_df['cov2']/covs_df['cov2'].sum()
covs_df['geometry'] = covs_df['geometry'].apply(wkt.loads)
covs_df = gpd.GeoDataFrame(covs_df, geometry='geometry')

for i in range(0,len(covs_df) ):
    for j in range(0,len(data_df1_enero_18)):
        if covs_df['geometry'].iloc[i].contains(data_df1_enero_18['geometry'].iloc[j]) == True:
            data_df1_enero_18['cov1'].iloc[j] = covs_df['cov1'].iloc[i]
            data_df1_enero_18['cov2'].iloc[j] = covs_df['cov2'].iloc[i]
            data_df1_enero_18['cell'].iloc[j] = covs_df.index.values[i]
            
data_df1_enero_18.to_csv('union_dataframes.csv')

            
###########################################################################################
stop = timeit.default_timer()
execution_time = stop - start
print("2Da Parte: Program Executed in "+str(execution_time)) # It returns time in seconds               
            


# In[ ]:




