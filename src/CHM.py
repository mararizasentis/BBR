import numpy as np
import rasterio


def CHM(DTM, DSM, CHM_file):
    # open the DTM tiff file
    with rasterio.open(DTM) as src:
        DTM_file = src.read(1)

    # open the DSM tiff file
    with rasterio.open(DSM) as src:
        DSM_file = src.read(1)

    # compute the CHM by subtracting the DTM from the DSM
    CHM = DSM_file - DTM_file

    # introduce the minimum and maximum vine height to have a CHM layer     containing only the canopy height of the vineyard
    CHM[CHM > 2] = np.nan
    CHM[CHM < 0.5] = np.nan

    # set spatial characteristics of the CHM to mirror the DTM/DSM
    kwargs = src.meta
    kwargs.update(dtype=rasterio.float32, count=1)

    # save the CHM tiff file
    with rasterio.open(CHM_file, 'w', **kwargs) as dst:
        dst.write_band(1, CHM.astype(rasterio.float32))


