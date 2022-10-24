# NOBLE-ROT
The NOBLE-ROT algorithm is an open-source standard workflow based on phenological parameters for automatic *Botrytis cinerea* detection in vineyards.


## How to run the code?
The NOBLE-ROT software can be executed in script mode or cross-platform inside a Python interpreter, such as PyCharm (JetBrains s.r.o., Prague, Czech Republic). 

The first part of the code (see lines 6-12 in the main.py script) is provided by OpenDroneMap. Redirect to their [directory](https://github.com/OpenDroneMap/ODM) for further information on how to implement it. This pats generates the orthomosaics, the Digital Surface Models (DSM), and the Digital Terrain Models (DTM).

Afterward, the novelty of the NOBLE-ROT algorithm starts running. 

**The directories of each file should be modified in order to properly run the code

## Which inputs are required?
The following table summarizes the required inputs to implement the NOBLE-ROT algorithm. A description of each file required is provided, along with the script that requires the input file. 

| Name                     | Description                                                                        | Script            |
| ------------------------ | ---------------------------------------------------------------------------------- | ----------------- |
| Raw_images.tif           | Images as taken by the UAV                                                         | main.py           |
| ROI.shp                  | Region of Interest, study area                                                     | crop_extent.py    |
| Grid.shp                 | Plant-to-plant distance and the distance between rows, in this case (2.5 x 3 m)    | extract_values.py |
| Shadows_grid.shp         | Same as grid.shp, but projected for the shadows, see [link](https://oeno-one.eu/article/view/4639) for further information  | shadows.py |
| GT.shp                   | Ground Truth points with the location of the diseased plants                       | points_in_grid.py |
| Min and max vine height  | Minimum and maximum height of the vine plants                                      | CHM.py            |

## Which folders are necessary to run the code?
Inside the project's folder, in this case named FlexiGroBots, 4 folders are required:
1) Field_extent: 
2) Frame:
3) GT: it contains the ground truth shapefile with the locations of the diseased plants. 
4) outputs: this folder is subdivided into two folders (middle_product and Deliverables)

## What is the purpose of each function?
A brief description of the main function of each python script is provided in the following table. 

## Training dataset
To train the NOBLE-ROT software, a training dataset is made available. 

## Citation
OpenDroneMap Authors ODM - A command line toolkit to generate maps, point clouds, 3D models and DEMs from drone, balloon or kite images. OpenDroneMap/ODM GitHub Page 2020; https://github.com/OpenDroneMap/ODM


link to odm
You should have a folder with the orthomosaics inside, the new and the old one (train/test). 
Mention also the folders to have: outputs, frame, GT...

