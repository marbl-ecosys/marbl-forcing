import os
import yaml

import numpy as np

USER = os.environ['USER']

DATAROOT = f'/glade/work/{USER}'
os.environ['DATAROOT'] = DATAROOT

inputdata = '/glade/p/cesmdata/cseg/inputdata'

dirwork = f'{DATAROOT}/cesm_inputdata/work'
os.makedirs(dirwork, exist_ok=True)   

dirout = f'{DATAROOT}/cesm_inputdata'
os.makedirs(dirout, exist_ok=True)   

with open('datasets.yaml') as f:
    datasets = yaml.safe_load(f)

def sedfrac_file(grid):
    return f'{dirwork}/sedfrac.{grid}.nc'

# TODO: use svn export to get these out of input data repo
topography_files = {'POP_gx1v7': f'{inputdata}/ocn/pop/gx1v7/grid/topography_20161215.ieeei4', 
                    'POP_gx3v7': f'{inputdata}/ocn/pop/gx3v7/grid/topography_20100105.ieeei4',
                    'POP_tx0.1v3': f'{inputdata}/ocn/pop/tx0.1v3/grid/topography_20170718.ieeei4'}