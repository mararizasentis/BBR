from sklearn import cluster
from osgeo import gdal, osr, ogr, gdalconst
import struct
import numpy as np
import rasterio
import shutil
import rasterstats as rs
import geopandas as gpd


def copy_orthomosaic(original, target):
    shutil.copyfile(original, target)

def kmeans(dest):
    # Perform a kmeans classification with 5 clusters
    dataset = gdal.Open(dest, gdal.GA_Update)
    band = dataset.GetRasterBand(5)
    img = band.ReadAsArray()
    X = img.reshape((-1, 1))
    k_means = cluster.KMeans(n_clusters=5)
    k_means.fit(X)
    X_cluster = k_means.labels_
    X_cluster = X_cluster.reshape(img.shape)
    band.WriteArray(X_cluster)


def delete_bands(shadows_classified, dest):
    # Perform it for the NIR (band 5) and delete the rest of the bands
    fmttypes = {'Byte': 'B', 'UInt16': 'H', 'Int16': 'h', 'UInt32': 'I', 'Int32': 'i', 'Float32': 'f', 'Float64': 'd'}
    dataset = gdal.Open(dest)
    number_band = 5
    prj = dataset.GetProjection()
    band = dataset.GetRasterBand(number_band)
    geotransform = dataset.GetGeoTransform()
    driver = gdal.GetDriverByName("GTiff")
    columns, rows = (band.XSize, band.YSize)
    BandType = gdal.GetDataTypeName(band.DataType)
    raster = []

    for y in range(band.YSize):
        scanline = band.ReadRaster(0, y, band.XSize, 1, band.XSize, 1, band.DataType)
        values = struct.unpack(fmttypes[BandType] * band.XSize, scanline)
        raster.append(values)

    dst_ds = driver.Create(shadows_classified, columns, rows, 1,band.DataType)
    raster = [item for element in raster for item in element]
    raster = np.asarray(np.reshape(raster, (rows, columns)))
    dst_ds.GetRasterBand(1).WriteArray(raster)
    dst_ds.SetGeoTransform(geotransform)
    srs = osr.SpatialReference(wkt=prj)
    dst_ds.SetProjection(srs.ExportToWkt())



def polygonize(polygon_output, shadow_class):
    # Generate a vector file with the 5 classes
    raster = gdal.Open(shadow_class)
    band = raster.GetRasterBand(1)
    drv = ogr.GetDriverByName('ESRI Shapefile')
    outfile = drv.CreateDataSource(polygon_output)
    outlayer = outfile.CreateLayer('polygonized raster'
                                   , srs = None )
    newField = ogr.FieldDefn('DN', ogr.OFTReal)
    outlayer.CreateField(newField)
    gdal.Polygonize(band, None, outlayer, 0, [])

def crop_polygon(cropped_polygon, pol_dir):
    # Merge small polygons smaller than 5 pixels
    field = gpd.read_file(pol_dir)
    field.crs = "epsg:25829"
    mask = field.area > 5
    selected_field = field.loc[mask]
    selected_field.to_file(cropped_polygon)

def rasterize(raster, shadows_class, cropped_pol):
    # Convert the vector file to a raster file
    data = gdal.Open(shadows_class, gdalconst.GA_ReadOnly)
    geo_transform = data.GetGeoTransform()
    x_min = geo_transform[0]
    y_max = geo_transform[3]
    x_max = x_min + geo_transform[1] * data.RasterXSize
    y_min = y_max + geo_transform[5] * data.RasterYSize
    x_res = data.RasterXSize
    y_res = data.RasterYSize
    mb_v = ogr.Open(cropped_pol)
    mb_l = mb_v.GetLayer()
    pixel_width = geo_transform[1]
    target_ds = gdal.GetDriverByName('GTiff').Create(raster, x_res, y_res, 1, gdal.GDT_Byte)
    target_ds.SetGeoTransform((x_min, pixel_width, 0, y_min, 0, pixel_width))
    band = target_ds.GetRasterBand(1)
    NoData_value = -999999
    band.SetNoDataValue(NoData_value)
    band.FlushCache()
    gdal.RasterizeLayer(target_ds, [1], mb_l, options=["ATTRIBUTE=DN"])


def select_shadow(final_raster, final_raster_georef, raster_directory):
    # Select among the raster file the band that corresponds to the shadows
    with rasterio.open(raster_directory) as src:
        shadows = src.read(1)

    shadows[shadows > 1] = 0
    shadows[shadows < 1] = 0
    shadows[shadows == 1] = 1
    kwargs = src.meta
    kwargs.update(dtype=rasterio.float32, count=1)

    with rasterio.open(final_raster, 'w', **kwargs) as dst:
        dst.write_band(1, shadows.astype(rasterio.float32))

    gdal.Warp(final_raster_georef, final_raster, dstSRS='EPSG:25829')
