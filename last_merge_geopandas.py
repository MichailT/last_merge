import geopandas as gpd
import pandas as pd
import glob, os





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

   

    buffer_out = df.buffer(10,resolution=2 )
    print('Buffer out')

    fix_union = gpd.geoseries.GeoSeries([geom for geom in buffer_out.unary_union.geoms])
    print('fix union')
    

    buffer_in = fix_union.buffer(-10,resolution=2 )
    print('buffer in')
    
    
    single_buffer_in = buffer_in.explode(index_parts=True)
    print('explode')

    
    single_buffer_in['area'] = single_buffer_in['geometry'].area/10000 
    print('geometry')

    

    forest = single_buffer_in[single_buffer_in['area'] >= 5000]
    print('small areas')

    forest.to_file("/dbfs/mnt/strukturparametre/Forest_Denmark_2020_test.gpkg", layer='Forest_Denmark_2020', driver="GPKG")
    
    

last_merge()

