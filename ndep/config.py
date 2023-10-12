import os

USER = os.environ['USER']

DATAROOT = f'/glade/work/{USER}'

inputdata = '/glade/p/cesmdata/cseg/inputdata'

dirwork = f'{DATAROOT}/cesm_inputdata/work'
os.makedirs(dirwork, exist_ok=True)   

dirout = f'{DATAROOT}/cesm_inputdata'
os.makedirs(dirout, exist_ok=True)   
