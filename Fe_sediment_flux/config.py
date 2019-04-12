import os
import yaml

import numpy as np

USER = os.environ['USER']

DATAROOT = f'/glade/work/{USER}'
os.environ['DATAROOT'] = DATAROOT

dirwork = f'{DATAROOT}/cesm_inputdata/work'
os.makedirs(dirwork, exist_ok=True)   

dirout = f'{DATAROOT}/cesm_inputdata'
os.makedirs(dirout, exist_ok=True)   

with open('datasets.yaml') as f:
    datasets = yaml.safe_load(f)


def compute_vertical_grids():
    vert_grid_edges = {}
    vert_grid_center = {}
    for grid in ['POP_gx1v7', 'POP_gx3v7', 'POP_tx0.1v3']:
        vert_grid_file = f'../data/grids/{grid}_vert_grid.txt'
        tmp = np.loadtxt(vert_grid_file)
        dz = tmp[:, 0]
        depth_edges = np.concatenate(([0.],np.cumsum(dz)))
        vert_grid_edges[grid] = depth_edges
        vert_grid_center[grid] = depth_edges[0:-1] + 0.5 * dz

    return vert_grid_edges
    
def sedfrac_file(grid):
    return f'{dirwork}/sedfrac.{grid}.nc'


vert_grid_edges = compute_vertical_grids()