import fiona
import rasterio.mask

def crop_extent(orthomosaic, roi, DTM, DSM, or_crop, dt_crop, ds_crop):
    # Read the ROI shapefile
    with fiona.open(roi, "r") as shapefile:
        shapes = [feature["geometry"] for feature in shapefile]
    # Crop the orthomosaic to the ROI
    with rasterio.open(orthomosaic) as src:
        out_image, out_transform = rasterio.mask.mask(src, shapes, crop=True)
        out_meta = src.meta

    out_meta.update({"driver": "GTiff",
                     "height": out_image.shape[1],
                     "width": out_image.shape[2],
                     "transform": out_transform})
    # Save the cropped orthomosaic
    with rasterio.open(or_crop, "w", **out_meta) as dest:
        dest.write(out_image)

    with rasterio.open(DTM) as src:
        out_image, out_transform = rasterio.mask.mask(src, shapes, crop=True)
        out_meta = src.meta

    out_meta.update({"driver": "GTiff",
                     "height": out_image.shape[1],
                     "width": out_image.shape[2],
                     "transform": out_transform})

    with rasterio.open(dt_crop, "w", **out_meta) as dest:
        dest.write(out_image)

    with rasterio.open(DSM) as src:
        out_image, out_transform = rasterio.mask.mask(src, shapes, crop=True)
        out_meta = src.meta

    out_meta.update({"driver": "GTiff",
                     "height": out_image.shape[1],
                    "width": out_image.shape[2],
                    "transform": out_transform})

    with rasterio.open(ds_crop, "w", **out_meta) as dest:
        dest.write(out_image)


