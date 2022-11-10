
"""
Model exported as python.
Name : model
Group : 
With QGIS : 32202
"""


 

from math import sin
import os
import sys

import pandas as pd
import geopandas as gpd
import numpy as np

from osgeo import gdal
from osgeo import ogr
from osgeo import osr

import subprocess






print('--------final merge-------------------')



def last_merge():


    wd = os.getcwd()
    os.chdir("/home/martin/Michail/Temp/test/")
    subprocess.run(["ogrmerge.py", "-single", "-f", "GPKG", "-o", "/home/martin/Michail/Temp/Merged_Forest_summer_2020_test.gpkg", "*.gpkg"])
    os.chdir(wd)

         # Buffer_out_last

    merged_forest = gpd.read_file("/home/martin/Michail/Temp/Merged_Forest_summer_2020_test.gpkg", layer='merged')

    merged_gds= gpd.GeoDataFrame(merged_forest)

    buffer_out = merged_gds.buffer(10,resolution=2 )
    print('Buffer out')

    fix_union = gpd.geoseries.GeoSeries([geom for geom in buffer_out.unary_union.geoms])
    print('fix union')
    fix_union_utm = fix_union.set_crs('epsg:25832')

    buffer_in = fix_union_utm.buffer(-10,resolution=2 )
    print('buffer in')
    buffer_in_utm =  buffer_in.to_crs(epsg=25832)
    
    single_buffer_in = buffer_in_utm.explode(index_parts=True)
    print('explode')

    single_buffer_in.crs = 'epsg:25832'
    print(single_buffer_in.crs)

    single_buffer_in = gpd.GeoDataFrame(single_buffer_in)
    
    single_buffer_in['area'] = single_buffer_in['geometry'].area/10000 
    print('geometry')

    

    forest = single_buffer_in[single_buffer_in['area'] >= 5000]
    print('small areas')

    forest.to_file("/home/martin/Michail/Temp/Forest_Denmark_2020_test.gpkg", layer='Forest_Denmark_2020', driver="GPKG")
    
    

last_merge()

qgs.exitQgis()