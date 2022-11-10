import geopandas as gpd
import pandas as pd
import glob, os
from shapely.geometry import Point, Polygon
from shapely.geometry import shape
from shapely import geometry





print('--------final merge-------------------')



def last_merge():
    
    clips_dir = '/dbfs/mnt/strukturparametre/test_2/' #folder with 53 geopackages forest clips

    gpkg_pattern = os.path.join(clips_dir, '*.gpkg')
    file_list = glob.glob(gpkg_pattern)

     #merge geopackages as geodataframes
        
    dfs = []
    for file in file_list:
        forest=gpd.read_file(file)
        gdf_forest = gpd.GeoDataFrame(forest)

        dfs.append(gdf_forest)
        
    df = pd.concat(dfs)  #merged geodataframes in data frame
    
    gdf = gpd.GeoDataFrame(df)

    gdf = gdf.to_crs(epsg=25832)

   

    buffer_out = gdf.to_crs(25832).buffer(10)
    print('Buffer out')

    fix_union = gpd.geoseries.GeoSeries([geom for geom in buffer_out.unary_union.geoms])
    
    print('fix union')
    
    fix_union_utm = fix_union.set_crs('epsg:25832')

    buffer_in = fix_union_utm.buffer(-10,resolution=2 )
    print('buffer in')
    
    
    single_buffer_in = buffer_in.explode(index_parts=True)

    print('explode')

    single_buffer_gdf = gpd.GeoDataFrame(gpd.GeoSeries(single_buffer_in))
    
    single_buffer_gdf = single_buffer_gdf.rename(columns={0:'geometry'}).set_geometry('geometry')
    
    single_buffer_gdf['area_ha'] = single_buffer_gdf.area/10000
    print('area')

    

    forest = single_buffer_gdf[single_buffer_gdf['area_ha'] >= 5000]
    print('small areas')

    forest.to_file("/dbfs/mnt/strukturparametre/Forest_Denmark_2020_test.gpkg", layer='Forest_Denmark_2020', driver="GPKG")
    
    

last_merge()

