import rasterio
import numpy

def NDVI(orthomosaic_directory, NDVI_output):
  # Load the orthomosaic and compute the NDVI
  with rasterio.open(orthomosaic_directory) as src:
    numpy.seterr(divide='ignore', invalid='ignore')
    NDVI = (src.read(4)-src.read(3))/(src.read(4)+src.read(3))
    NDVI[NDVI > 1] = 0
    NDVI[NDVI < -1] = 0
  kwargs = src.meta
  kwargs.update(dtype=rasterio.float32, count=1)
  with rasterio.open(NDVI_output, 'w', **kwargs) as dst:
    dst.write_band(1, NDVI.astype(rasterio.float32))


def crop_NDVI(NDVI_clipped, CHM_file, NDVI_output):
    # Crop the NDVI map to the extent of the Canopy Height Model to have only the NDVI of the vineyard plants
    with rasterio.open(NDVI_clipped) as src:
        NDVI = src.read(1)
    with rasterio.open(CHM_file) as src:
        CHM = src.read(1)
    CHM[CHM == 0] = -1
    CHM[CHM > 0] = 0
    trial = NDVI - CHM
    trial[trial >= 1] = 0
    trial[trial < 0] = 0
    kwargs = src.meta
    kwargs.update(dtype=rasterio.float32, count=1)
    with rasterio.open(NDVI_output, 'w', **kwargs) as dst:
        dst.write_band(1, trial.astype(rasterio.float32))
