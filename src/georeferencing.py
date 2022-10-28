from osgeo import gdal

# Georeference the orthomosaic, DTM, and DSM to the desired EPSG code
def georeferencing(input_ortho, output_ortho, input_dtm, output_dtm, input_dsm, output_dsm):
    gdal.Warp(output_ortho, input_ortho , dstSRS='EPSG:25829')
    gdal.Warp(output_dtm, input_dtm, dstSRS='EPSG:25829')
    gdal.Warp(output_dsm, input_dsm, dstSRS='EPSG:25829')
