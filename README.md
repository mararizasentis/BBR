# NOBLE-ROT algorithm
The NOBLE-ROT algorithm is an open-source standard workflow based on phenological parameters for automatic *Botrytis cinerea* detection in vineyards.


## How to run the code?
The NOBLE-ROT software can be executed in script mode or cross-platform inside a Python interpreter, such as PyCharm (JetBrains s.r.o., Prague, Czech Republic). 

The first part of the code (see lines 6-12 in the main.py script) is provided by OpenDroneMap. Redirect to their [directory](https://github.com/OpenDroneMap/ODM) for further information on how to implement it. This pats generates the orthomosaics, the Digital Surface Models (DSM), and the Digital Terrain Models (DTM).

Afterward, the novelty of the NOBLE-ROT algorithm starts running. 

\*The directories of each file should be modified in order to properly run the code

## Which inputs are required?
The following table summarizes the required inputs to implement the NOBLE-ROT algorithm. A description of each file required is provided, along with the script that requires the input file. 

| Name                     | Description                                                                        | Script            |
| ------------------------ | ---------------------------------------------------------------------------------- | ----------------- |
| Raw_images.tif           | Images as taken by the UAV                                                         | main.py           |
| ROI.shp                  | Region of Interest, study area                                                     | crop_extent.py    |
| Grid.shp                 | Plant-to-plant distance and the distance between rows, in this case (2.5 x 3 m)    | extract_values.py |
| Shadows_grid.shp         | Same as grid.shp, but projected for the shadows, see [link](https://oeno-one.eu/article/view/4639) for further information  | shadows.py |
| GT.shp                   | Ground Truth points with the location of the diseased plants                       | points_in_grid.py |
| EPSG code                | EPSG code to which the Region of Interest is georeferenced                         | georeferencing.py |
| Min and max vine height  | Minimum and maximum height of the vine plants                                      | CHM.py            |

## Which folders are necessary to run the code?
Inside the project's folder, in this case named FlexiGroBots, 4 folders are required:
1) Field_extent: it includes the shapefile of the Region of Interest (ROI).
2) Frame: two shapefile grids are included in this folder. The first grid refers to the plant-to-plnt distance and the distance between rows. The second one is the shadows grid (see table above). 
3) GT: it contains the ground truth shapefile with the locations of the diseased plants. 
4) outputs: this folder is subdivided into two folders (middle_product and Deliverables)

## What is the purpose of each function?
A brief description of the main function of each python script is provided in the following table. 

| Script                     | Functionality                                                                                                               |
| -------------------------- | -------------------------------------------------------------------------------------------------------------------------   |
| main.py                    | (1)	Generate the orthomosaics, DSM, and  DTM, and (2)  Run the whole algorithm at once by calling the rest of the scripts  |           
| georeferencing.py          | Georeference of the orthomosaic, DSM, and DTM to the appropriate EPSG code                                                  | 
| crop_extent.py             | Mask the orthomosaic, DSM, and DTM to the Region of Interest                                                                | 
| CHM.py                     | Generate the Canopy Height Model of the vineyard                                                                            | 
| NDVI.py                    | Compute the NDVI of the vineyard                                                                                            | 
| shadows.py                 | Extract the shadows area to estimate the Leaf Area Index                                                                    | 
| extract_values.ppy         | Apply zonal statistics at plant-level                                                                                       | 
| botrytis_classification.py | Select the plants which are not affected by botrytis                                                                        |
| points_in_grid.py          | Select which plants are affected by botrytis thanks to ground truth information                                             | 
| join_stats_disease.py      | Join the zonal statistics results with the health status information (Botrytis, no Botrytis)                                | 
| randomForest.py            | Train/test the Random Forest algorithm for botrytis detection                                                               | 
| heatmap.py                 | Generate a heatmap with the hotspots of the potential risk of *Botrytis cinerea*                                            | 
| PDF.py                     | Generate a PDF report informing about the potential risk of *Botrytis cinerea*                                              | 

## Available dataset
To train or validate the NOBLE-ROT software, a dataset [dataset](https://zenodo.org/record/7064895#.Y1ZZMnZBxPZ) is made available. 

## Citation
NOBLE-ROT algorithm - An open-source standard workflow based on phenological crop parameters for automatic Botrytis cinerea detection in vineyards. mararizasentis/NOBLE-ROT GitHub Page 2022; https://github.com/mararizasentis/NOBLE-ROT


