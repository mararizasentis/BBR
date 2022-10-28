import geopandas
import pandas as pd
from shapely.geometry import Point, Polygon


def points_in_grid(grid_directory, gt_points_directory, diseased):
    # Read the grid provided by the user
    grid = geopandas.GeoDataFrame.from_file(grid_directory)
    # Read the GT points
    gt_points = geopandas.GeoDataFrame.from_file(gt_points_directory)
    plant = []
    disease = []
    # Select which plants of the grid are affected by Botrytis
    for i in grid["geometry"]:
        for j in gt_points["geometry"]:
            if Polygon(i).contains(Point(j)):
                index = grid[grid["geometry"] == i].index[0]
                plant.append(grid["plantID"][index])
                disease.append("Botrytis")
    # Geneate a "disease plants" dataset
    diseased_plants_old = pd.DataFrame(list(zip(plant, disease)), columns=["plantID", "status"])
    diseased_plants = diseased_plants_old.drop_duplicates()
    diseased_plants.to_csv(diseased)
