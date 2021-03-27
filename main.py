from podpac.datalib.terraintiles import TerrainTiles
from podpac import Coordinates, clinspace
import matplotlib.pyplot as plt
import numpy as np
import json
import csv
import pandas as pd
import time
from copy import deepcopy
from podpac.managers import aws


N = 2000
POINTS_NUM = 10
GRID = int(N / POINTS_NUM)
# getting data from terrain tiles dataset with podapac
terrain_node = TerrainTiles(tile_format='geotiff', zoom=7)
# Europe's coordinates
coords = Coordinates([clinspace(71, 35, N), clinspace(-9, 30, N)], dims=['lat', 'lon'])

# node = podpac.managers.aws.Lambda(source=terrain_node)

o = terrain_node.eval(coords)
data_from_tt = np.asarray(o.data)
# original data -> plotting
initial_data = deepcopy(data_from_tt)
# copied data -> calculations
_, h = initial_data.shape
# initial data -> (2000, 2000)
# grid_tiles -> (40000, 10, 10)
grid_tiles = initial_data.reshape(h//POINTS_NUM, POINTS_NUM, -1, POINTS_NUM).swapaxes(1, 2).reshape(-1, POINTS_NUM, POINTS_NUM)
# calculating mean height value in every region
mean_heights = []
for x in grid_tiles:
    mean_heights.append((np.max(x) - np.min(x)) / 2)
mean_heights = np.asarray(mean_heights)
# making data fit the grid
mean_heights = mean_heights.reshape(GRID, GRID)
# assigning average height to every measuring point in its region  
final_heights = np.repeat(mean_heights, POINTS_NUM, axis=0)
final_heights = np.repeat(final_heights, POINTS_NUM, axis=1)

# mask to display only height's change over 500
# masked_result = pd.DataFrame(final_heights)
# masked_result.mask(final_heights > 500)

# plotting results -> grid data and height's changes in Europe

# saving our final results to csv file
np.savetxt('results.csv', final_heights, delimiter=',')

plt.subplot(121)
plt.title("Grid of input data")
plt.imshow(data_from_tt, cmap='hot')
plt.subplot(122)
plt.title("Results")
plt.imshow(final_heights, cmap='hot')
plt.subplots_adjust(bottom=0.1, right=0.8, top=0.9)
cax = plt.axes([0.85, 0.1, 0.04, 0.7])
plt.colorbar(cax=cax)
plt.legend()

# saving our results to svg
plt.savefig('result.svg')

plt.show()
