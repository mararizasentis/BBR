# NOBLE-ROT
The NOBLE-ROT algorithm is an open-source standard workflow based on phenological parameters for automatic *Botrytis cinerea* detection in vineyards.


## How to run the code?
The NOBLE-ROT software can be executed in script mode or cross-platform inside a Python interpreter, such as PyCharm (JetBrains s.r.o., Prague, Czech Republic). 

The first part of the code is provided by OpenDroneMap. Redirect to their [directory](https://github.com/OpenDroneMap/ODM) for further information on how to implement it. 

## Which inputs are required?
The following table summarizes the required inputs to implement the NOBLE-ROT algorithm. A description of each file required is provided, along with the script that requires the input file. 

| Name                     | Description                                                                        | Script            |
| ------------------------ | ---------------------------------------------------------------------------------- | ----------------- |
| Raw_images.tif           | Images as taken by the UAV                                                         | main.py           |
| ROI.shp                  | Region of Interest, study area                                                     | crop_extent.py    |
| Grid.shp                 | Plant-to-plant distance and the distance between rows, in this case (2.5 x 3 m)    | extract_values.py |
| Shadows_grid.shp         | Same as grid.shp, but projected for the shadows, see [18] for further information  | shadows.py        |
| GT.shp                   | Ground Truth points with the location of the diseased plants                       | points_in_grid.py |
| Min and max vine height  | Minimum and maximum height of the vine plants                                      | CHM.py            |




link to odm
You should have a folder with the orthomosaics inside, the new and the old one (train/test). 
Mention also the folders to have: outputs, frame, GT...

Add Table 3 in the readme, to provide insights of the purpose of each function
