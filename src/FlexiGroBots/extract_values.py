import rasterstats as rs
import geopandas as gpd
import rasterio
import pandas as pd
from functools import reduce

def extract_values(NDVI, DTM, CHM, plots, CSV_dir):
    # Load the DTM raster file
    DTM_transform = rasterio.open(DTM)

    # Compute statistics at plant level
    plot_NDVI = rs.zonal_stats(plots,
                         NDVI,
                         nodata=0,
                         affine=DTM_transform.transform,
                         geojson_out=True,
                         copy_properties=True,
                         stats="count min mean max median std")

    # Generate a GeoDataFrame with the relevant information
    df_NDVI = gpd.GeoDataFrame.from_features(plot_NDVI)
    df_NDVI.drop(["geometry", "fid"], axis=1, inplace=True)
    df_NDVI.columns = [str(col) + "_NDVI" for col in df_NDVI.columns]
    df_NDVI.rename(columns={'plantID_NDVI':'plantID'}, inplace=True)

    plot_DTM = rs.zonal_stats(plots,
                             DTM,
                             nodata=0,
                             affine=DTM_transform.transform,
                             geojson_out=True,
                             copy_properties=True,
                             stats="min mean max median std")


    df_DTM = gpd.GeoDataFrame.from_features(plot_DTM)
    df_DTM.drop(["geometry", "fid"], axis=1, inplace=True)
    df_DTM.columns = [str(col) + "_DTM" for col in df_DTM.columns]
    df_DTM.rename(columns={'plantID_DTM':'plantID'}, inplace=True)

    plot_CHM = rs.zonal_stats(plots,
                              CHM,
                              nodata=0,
                              affine=DTM_transform.transform,
                              geojson_out=True,
                              copy_properties=True,
                              stats="count min mean max median std")

    df_CHM = gpd.GeoDataFrame.from_features(plot_CHM)
    df_CHM.drop(["geometry", "fid"], axis=1, inplace=True)
    df_CHM.columns = [str(col) + "_CHM" for col in df_CHM.columns]
    df_CHM.rename(columns={'plantID_CHM':'plantID'}, inplace=True)

    # Merge the datasets into one
    dfs = [df_NDVI, df_DTM, df_CHM]
    df_final = reduce(lambda left,right: pd.merge(left, right, on="plantID"), dfs)
    list = ["min_CHM",	"mean_CHM",	"max_CHM", "median_CHM", "std_CHM", "min_NDVI",	"mean_NDVI",
             "max_NDVI", "median_NDVI", "std_NDVI"]

    # Generate a CSV file with the extracted statistics
    [df_final[i].fillna(0, inplace=True) for i in df_final[list]]
    df_final.to_csv(CSV_dir)


def extract_values_shadows(shadows, grid, DTM, shadow_CSV):
    # Load the DTM raster file
    DTM_transform = rasterio.open(DTM)

    # Compute statistics at plant level
    plot_shadows = rs.zonal_stats(grid,
                                shadows,
                                nodata=0,
                                affine=DTM_transform.transform,
                                geojson_out=True,
                                copy_properties=True,
                                stats="count")

    # Generate a GeoDataFrame with the relevant information
    df_Shadow = gpd.GeoDataFrame.from_features(plot_shadows)
    df_Shadow.drop(["geometry", "fid"], axis=1, inplace=True)
    df_Shadow.columns = [str(col) + "_shadow" for col in df_Shadow.columns]
    df_Shadow.rename(columns={'plantID_shadow': 'plantID'}, inplace=True)
    df_Shadow.to_csv(shadow_CSV)


def merge_dataframes(dataframe1, dataframe2, CSV):
    # Merge both datasets and transform the final one to a CSV file
    df = pd.merge(pd.read_csv(dataframe1), pd.read_csv(dataframe2), on="plantID")
    df.drop(["Unnamed: 0_y", "Unnamed: 0_x"], axis=1, inplace=True)
    df.to_csv(CSV)


