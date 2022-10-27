# NOBLE-ROT ALGORITHM

# Import the necessary libraries
import pandas as pd
import subprocess
res = subprocess.Popen(["docker", "run","--rm", "-v", "/home/saidlab/PycharmProjects/orthomosaics/old_orthomosaic/datasets:/datasets", "opendronemap/odm",
                            "--project-path", "/datasets/project/", "--dsm", "--dtm", "--feature-quality", "ultra",
                            "--ignore-gsd", "--skip-report"])
if res.wait() == 0:
    res2 = subprocess.Popen(["docker", "run","--rm", "-v", "/home/saidlab/PycharmProjects/orthomosaics/new_orthomosaic/datasets2:/datasets2", "opendronemap/odm",
                                "--project-path", "/datasets2/project2/", "--dsm", "--dtm", "--feature-quality", "ultra",
                                "--ignore-gsd", "--skip-report"])

    if res2.wait() == 0:

        # Georeferencing the orthomosaics generated with ODM
        from georeferencing import georeferencing
        ortho_input = "/home/saidlab/PycharmProjects/orthomosaics/new_orthomosaic/datasets2/project2/code/odm_orthophoto/odm_orthophoto.tif"
        ortho_output = "/home/saidlab/PycharmProjects/FlexiGroBots/outputs/middle_product/new_ortho_georeferenced.tif"
        dtm_input = "/home/saidlab/PycharmProjects/orthomosaics/new_orthomosaic/datasets2/project2/code/odm_dem/dtm.tif"
        dtm_output = "//home/saidlab/PycharmProjects/FlexiGroBots/outputs/middle_product/new_dtm_georeferenced.tif"
        dsm_input = "/home/saidlab/PycharmProjects/orthomosaics/new_orthomosaic/datasets2/project2/code/odm_dem/dsm.tif"
        dsm_output = "/home/saidlab/PycharmProjects/FlexiGroBots/outputs/middle_product/new_dsm_georeferenced.tif"
        georeferencing(ortho_input, ortho_output, dtm_input, dtm_output, dsm_input, dsm_output)

        ortho_input2 = "/home/saidlab/PycharmProjects/orthomosaics/old_orthomosaic/datasets/project/code/odm_orthophoto/odm_orthophoto.tif"
        ortho_output2 = "/home/saidlab/PycharmProjects/FlexiGroBots/outputs/middle_product/old_ortho_georeferenced.tif"
        dtm_input2 = "/home/saidlab/PycharmProjects/orthomosaics/old_orthomosaic/datasets/project/code/odm_dem/dtm.tif"
        dtm_output2 = "/home/saidlab/PycharmProjects/FlexiGroBots/outputs/middle_product/old_dtm_georeferenced.tif"
        dsm_input2 = "/home/saidlab/PycharmProjects/orthomosaics/old_orthomosaic/datasets/project/code/odm_dem/dsm.tif"
        dsm_output2 = "/home/saidlab/PycharmProjects/FlexiGroBots/outputs/middle_product/old_dsm_georeferenced.tif"
        georeferencing(ortho_input2, ortho_output2, dtm_input2, dtm_output2, dsm_input2, dsm_output2)

        # Crop the extent of the products generated
        from crop_extent import crop_extent
        roi_directory = "/home/saidlab/PycharmProjects/FlexiGroBots/Field_extent/RoI.shp"
        ortho_crop = "/home/saidlab/PycharmProjects/FlexiGroBots/outputs/middle_product/new_ortho_clipped.tif"
        dtm_crop = "/home/saidlab/PycharmProjects/FlexiGroBots/outputs/middle_product/new_dtm_clipped.tif"
        dsm_crop = "/home/saidlab/PycharmProjects/FlexiGroBots/outputs/middle_product/new_dsm_clipped.tif"
        crop_extent(ortho_output, roi_directory, dtm_output, dsm_output, ortho_crop, dtm_crop, dsm_crop)

        ortho_crop2 = "/home/saidlab/PycharmProjects/FlexiGroBots/outputs/middle_product/old_ortho_clipped.tif"
        dtm_crop2 = "/home/saidlab/PycharmProjects/FlexiGroBots/outputs/middle_product/old_dtm_clipped.tif"
        dsm_crop2 = "/home/saidlab/PycharmProjects/FlexiGroBots/outputs/middle_product/old_dsm_clipped.tif"
        crop_extent(ortho_output2, roi_directory, dtm_output2, dsm_output2, ortho_crop2, dtm_crop2, dsm_crop2)

        # Generate the CHM
        from CHM import CHM
        dtm_crop = "/home/saidlab/PycharmProjects/FlexiGroBots/outputs/middle_product/new_dtm_clipped.tif"
        dsm_crop = "/home/saidlab/PycharmProjects/FlexiGroBots/outputs/middle_product/new_dsm_clipped.tif"
        CHM_output = "/home/saidlab/PycharmProjects/FlexiGroBots/outputs/middle_product/new_CHM.tif"
        CHM(dtm_crop, dsm_crop, CHM_output)

        dtm_crop2 = "/home/saidlab/PycharmProjects/FlexiGroBots/outputs/middle_product/old_dtm_clipped.tif"
        dsm_crop2 = "/home/saidlab/PycharmProjects/FlexiGroBots/outputs/middle_product/old_dsm_clipped.tif"
        CHM_output2 = "/home/saidlab/PycharmProjects/FlexiGroBots/outputs/middle_product/old_CHM.tif"
        CHM(dtm_crop2, dsm_crop2, CHM_output2)

        # Generate the NDVI
        from NDVI import NDVI
        inFilePath = "/home/saidlab/PycharmProjects/FlexiGroBots/outputs/middle_product/new_ortho_clipped.tif"
        outFilePath = "/home/saidlab/PycharmProjects/FlexiGroBots/outputs/middle_product/new_NDVI_clipped.tif"
        NDVI(inFilePath, outFilePath)

        inFilePath2 = "/home/saidlab/PycharmProjects/FlexiGroBots/outputs/middle_product/old_ortho_clipped.tif"
        outFilePath2 = "/home/saidlab/PycharmProjects/FlexiGroBots/outputs/middle_product/old_NDVI_clipped.tif"
        NDVI(inFilePath2, outFilePath2)

        from NDVI import crop_NDVI
        CHM_out = "/home/saidlab/PycharmProjects/FlexiGroBots/outputs/middle_product/new_CHM.tif"
        NDVI_final = "/home/saidlab/PycharmProjects/FlexiGroBots/outputs/middle_product/new_NDVI_cropped.tif"
        crop_NDVI(outFilePath, CHM_out, NDVI_final)

        CHM_out2 = "/home/saidlab/PycharmProjects/FlexiGroBots/outputs/middle_product/old_CHM.tif"
        NDVI_final2 = "/home/saidlab/PycharmProjects/FlexiGroBots/outputs/middle_product/old_NDVI_cropped.tif"
        crop_NDVI(outFilePath2, CHM_out2, NDVI_final2)

        # Detect the shadows to get the LAI
        from shadows import copy_orthomosaic
        destiny = r"/home/saidlab/PycharmProjects/FlexiGroBots/outputs/middle_product/new_kmeans_shadows.tif"
        copy_orthomosaic(inFilePath, destiny)

        destiny2 = r"/home/saidlab/PycharmProjects/FlexiGroBots/outputs/middle_product/old_kmeans_shadows.tif"
        copy_orthomosaic(inFilePath2, destiny2)

        from shadows import kmeans
        kmeans(destiny)
        kmeans(destiny2)

        from shadows import delete_bands
        shadows_classification = "/home/saidlab/PycharmProjects/FlexiGroBots/outputs/middle_product/new_shadows_classified.tif"
        delete_bands(shadows_classification, destiny)

        shadows_classification2 = "/home/saidlab/PycharmProjects/FlexiGroBots/outputs/middle_product/old_shadows_classified.tif"
        delete_bands(shadows_classification2, destiny2)

        from shadows import polygonize
        polygon_dir = "/home/saidlab/PycharmProjects/FlexiGroBots/outputs/middle_product/new_shadows_polygon.shp"
        polygonize(polygon_dir, shadows_classification)

        polygon_dir2 = "/home/saidlab/PycharmProjects/FlexiGroBots/outputs/middle_product/old_shadows_polygon.shp"
        polygonize(polygon_dir2, shadows_classification2)

        from shadows import crop_polygon
        cropped_polygon = "/home/saidlab/PycharmProjects/FlexiGroBots/outputs/middle_product/new_cropped_polygon.shp"
        crop_polygon(cropped_polygon, polygon_dir)

        cropped_polygon2 = "/home/saidlab/PycharmProjects/FlexiGroBots/outputs/middle_product/old_cropped_polygon.shp"
        crop_polygon(cropped_polygon2, polygon_dir2)

        from shadows import rasterize
        raster_dir = "/home/saidlab/PycharmProjects/FlexiGroBots/outputs/middle_product/new_shadows_raster.tif"
        rasterize(raster_dir, shadows_classification, cropped_polygon)

        raster_dir2 = "/home/saidlab/PycharmProjects/FlexiGroBots/outputs/middle_product/old_shadows_raster.tif"
        rasterize(raster_dir2, shadows_classification2, cropped_polygon2)

        from shadows import select_shadow
        raster_final = "/home/saidlab/PycharmProjects/FlexiGroBots/outputs/middle_product/new_final_shadows.tif"
        raster_final_georef = "/home/saidlab/PycharmProjects/FlexiGroBots/outputs/middle_product/new_final_shadows_georef.tif"
        select_shadow(raster_final, raster_final_georef, raster_dir)

        raster_final2 = "/home/saidlab/PycharmProjects/FlexiGroBots/outputs/middle_product/old_final_shadows.tif"
        raster_final_georef2 = "/home/saidlab/PycharmProjects/FlexiGroBots/outputs/middle_product/old_final_shadows_georef.tif"
        select_shadow(raster_final2, raster_final_georef2, raster_dir2)

        # Extract general statistics of the variables above within a grid
        from extract_values import extract_values
        plots_dir = "/home/saidlab/PycharmProjects/FlexiGroBots/Frame/Grid.shp"
        CSV = "/home/saidlab/PycharmProjects/FlexiGroBots/outputs/middle_product/new_partial_stats.csv"
        CSV2 = "/home/saidlab/PycharmProjects/FlexiGroBots/outputs/middle_product/old_partial_stats.csv"
        extract_values(NDVI_final, dtm_output, CHM_output, plots_dir, CSV)
        extract_values(NDVI_final2, dtm_output2, CHM_output2, plots_dir, CSV2)

        from extract_values import extract_values_shadows
        shadows_grid = "/home/saidlab/PycharmProjects/FlexiGroBots/Frame/Grid_shadows.shp"
        CSV_shadow = "/home/saidlab/PycharmProjects/FlexiGroBots/outputs/middle_product/new_shadow_stats.csv"
        extract_values_shadows(raster_final_georef, shadows_grid, dtm_output, CSV_shadow)

        CSV_shadow2 = "/home/saidlab/PycharmProjects/FlexiGroBots/outputs/middle_product/old_shadow_stats.csv"
        extract_values_shadows(raster_final_georef2, shadows_grid, dtm_output2, CSV_shadow2)

        from extract_values import merge_dataframes
        final_CSV = "/home/saidlab/PycharmProjects/FlexiGroBots/outputs/middle_product/new_final_stats.csv"
        merge_dataframes(CSV, CSV_shadow, final_CSV)

        final_CSV2 = "/home/saidlab/PycharmProjects/FlexiGroBots/outputs/middle_product/old_final_stats.csv"
        merge_dataframes(CSV2, CSV_shadow2, final_CSV2)

        # Classify the diseased and non-diseased plants
        from botrytis_classification import select_non_botrytis_plants
        disease = "/home/saidlab/PycharmProjects/FlexiGroBots/outputs/middle_product/new_disease_list.csv"
        filter = "/home/saidlab/PycharmProjects/FlexiGroBots/outputs/middle_product/input_test_randomForest.csv"
        select_non_botrytis_plants(final_CSV, disease, filter)

        disease2 = "/home/saidlab/PycharmProjects/FlexiGroBots/outputs/middle_product/old_disease_list.csv"
        filter2 = "/home/saidlab/PycharmProjects/FlexiGroBots/outputs/middle_product/old_final_stats_filtered.csv"
        select_non_botrytis_plants(final_CSV2, disease2, filter2)

        # Get diseased points from the grid
        from points_in_grid import points_in_grid
        gt_points_dir = "/home/saidlab/PycharmProjects/FlexiGroBots/GT/20210916_flexigrobots.shp"
        diseased_plants = "/home/saidlab/PycharmProjects/FlexiGroBots/outputs/middle_product/old_diseased_plants.csv"
        points_in_grid(plots_dir, gt_points_dir, diseased_plants)

        # Join all the datasets
        from join_stats_disease import final_stats_table
        input_random = "/home/saidlab/PycharmProjects/FlexiGroBots/outputs/middle_product/input_train_randomForest.csv"
        final_stats_table(pd.read_csv(final_CSV2), pd.read_csv(diseased_plants), pd.read_csv(disease2), input_random)

        # Train and test the randomForest algorithm
        from randomForest import randomForestBotrytis
        output_RF = "/home/saidlab/PycharmProjects/FlexiGroBots/outputs/middle_product/output_RF.csv"
        randomForestBotrytis(input_random, filter, output_RF)

        from heatmap import affected_points
        heatmap_dir = "/home/saidlab/PycharmProjects/FlexiGroBots/outputs/middle_product/heatmap.tif"
        botrytis_points = "/home/saidlab/PycharmProjects/FlexiGroBots/outputs/middle_product/Botrytis_points.shp"
        affected_points(plots_dir, output_RF, botrytis_points, heatmap_dir)

        from heatmap import heatmap_normalization
        heatmap_normalized_dir = "/home/saidlab/PycharmProjects/FlexiGroBots/outputs/middle_product/heatmap_normalized.tif"
        heatmap_normalization(heatmap_dir, heatmap_normalized_dir)

        from heatmap import extract_values
        heatmap_shp =  "/home/saidlab/PycharmProjects/FlexiGroBots/outputs/Deliverables/heatmap.shp"
        heatmap_csv = "/home/saidlab/PycharmProjects/FlexiGroBots/outputs/Deliverables/heatmap_CSIC.csv"
        extract_values(plots_dir, heatmap_normalized_dir, heatmap_csv, heatmap_shp)

        # Generate the Botrytis assessment report in PDF
        from PDF import TIF_to_PNG
        CHM_report = "/home/saidlab/PycharmProjects/FlexiGroBots/outputs/middle_product/CHM.png"
        NDVI_report = "/home/saidlab/PycharmProjects/FlexiGroBots/outputs/middle_product/NDVI.png"
        heatmap_report = "/home/saidlab/PycharmProjects/FlexiGroBots/outputs/middle_product/heatmap.png"
        ortho_report = "/home/saidlab/PycharmProjects/FlexiGroBots/outputs/middle_product/orthomosaic.png"
        TIF_to_PNG(CHM_output, CHM_report, NDVI_final, NDVI_report, ortho_output, ortho_report, heatmap_normalized_dir, heatmap_report)

        from PDF import generate_PDF
        report = "/home/saidlab/PycharmProjects/FlexiGroBots/outputs/Deliverables/Botrytis_report.pdf"
        generate_PDF(report, ortho_report,NDVI_report, CHM_report, heatmap_report)