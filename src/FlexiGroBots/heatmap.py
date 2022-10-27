import geopandas as gpd
import pandas as pd
from spatial_kde import spatial_kernel_density
import rasterio
import rasterstats as rs


def affected_points(grid_shp, diseased_plants_csv, botrytis_shp, heatmap_tif):
    # Read the grid shapefile
    grid = gpd.read_file(grid_shp)
    # Read the CSV file containing the diseased plants
    diseased_plants = pd.read_csv(diseased_plants_csv)
    diseased_plants.columns = ["ID","plantID", "prediction"]
    # Merge both data sources
    merged_dataset = grid.merge(diseased_plants, on="plantID")
    # Select only the plants affected by Botrytis and compute the centroid of the polyogn
    filter = merged_dataset[merged_dataset["prediction"] == "Botrytis"].centroid
    filter.to_file(botrytis_shp)
    data = gpd.read_file(botrytis_shp)
    # Generate the heatmap thanks to the kernel density function
    spatial_kernel_density(data, radius = 15, output_pixel_size=0.1, output_path=heatmap_tif, output_driver="GTiff")


def heatmap_normalization(heatmap_tif, heatmap_normalized_tif):
    # Read the heatmap file
    heatmap = rasterio.open(heatmap_tif).read()
    # Select the maximum and minimum value (0)
    max_value = heatmap.max()
    min_value = 0
    # Normalize the values of the heatmap file
    heatmap_normalized = (heatmap-min_value)/max_value
    heatmap_normalized[heatmap_normalized < 0] = 0
    with rasterio.open(heatmap_tif) as src:
        heatmap_reading = src.read(1)
    kwargs = src.meta
    kwargs.update(dtype=rasterio.float32, count=1)
    #Save the normalized heatmap
    with rasterio.open(heatmap_normalized_tif, 'w', **kwargs) as dst:
          dst.write(heatmap_normalized.astype(rasterio.float32))


def extract_values(grid, heatmap_normalized_tif, CSIC_csv, CSIC_shp):
    # Extract relevant statistics
    plot_heatmap= rs.zonal_stats(grid,
                         heatmap_normalized_tif,
                         #nodata=0,
                         geojson_out=True,
                         copy_properties=True,
                         stats="min mean max median std")

    # Transform the normalized heatmap to a shapefile and CSV file
    df_heatmap = gpd.GeoDataFrame.from_features(plot_heatmap)
    df_heatmap.drop(["fid"], axis=1, inplace=True)
    df_heatmap.columns = [str(col) + "_heatmap" for col in df_heatmap.columns]
    df_heatmap.rename(columns={'plantID_heatmap':'plantID', "geometry_heatmap":"geometry"}, inplace=True)
    df_heatmap.replace(r'^s*$', float('NaN'), regex=True)
    df_heatmap.to_csv(CSIC_csv)
    df_heatmap.to_file(CSIC_shp, crs="EPSG:25829")