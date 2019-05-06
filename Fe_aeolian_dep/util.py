from itertools import product

import numpy as np
import cftime
import xarray as xr

eom_day_noleap = np.array([31., 28., 31., 30., 31., 30., 31., 31., 30., 31., 30., 31.])

def compute_grid_area(ds):

    Re = 6.37122e6 # m, radius of Earth

    # normalize area so that sum over 'lat', 'lon' yields area_earth
    area = ds.gw + 0.0 * ds.lon # add 'lon' dimension
    area = (4.0 * np.pi * Re**2 / area.sum(dim=('lat', 'lon'))) * area # m^2
    area.attrs['units'] = 'm^2'
    
    return area

def cpl_names_to_datm_names(ds):
    syn = {'a2x1d_Faxa_bcphiwet': 'BCDEPWET',
       'a2x1d_Faxa_bcphodry': 'BCPHODRY',
       'a2x1d_Faxa_bcphidry': 'BCPHIDRY',
       'a2x1d_Faxa_ocphiwet': 'OCDEPWET',
       'a2x1d_Faxa_ocphidry': 'OCPHIDRY',
       'a2x1d_Faxa_ocphodry': 'OCPHODRY',
       'a2x1d_Faxa_dstwet1': 'DSTX01WD',
       'a2x1d_Faxa_dstdry1': 'DSTX01DD',
       'a2x1d_Faxa_dstwet2': 'DSTX02WD',
       'a2x1d_Faxa_dstdry2': 'DSTX02DD',
       'a2x1d_Faxa_dstwet3': 'DSTX03WD',
       'a2x1d_Faxa_dstdry3': 'DSTX03DD',
       'a2x1d_Faxa_dstwet4': 'DSTX04WD',
       'a2x1d_Faxa_dstdry4': 'DSTX04DD'}
        
    for vcpl, vdatm in syn.items():
        if vcpl in ds.data_vars:
            ds = ds.rename({vcpl: vdatm})
    
    return ds

def time_mid_mon(years):
    mid_mon = eom_day_noleap / 2 + 1.
    mid_mon_day = np.floor(mid_mon)
    mid_mon_hr  = (mid_mon - mid_mon_day) * 24
    return [cftime.DatetimeNoLeap(year, mon, mid_mon_day[mon-1], mid_mon_hr[mon-1]) 
            for year, mon in product(years, range(1, 13))]

def time_bnds_mon(years):
    return xr.DataArray(np.array([[cftime.date2num(cftime.DatetimeNoLeap(year, mon, 1), 
                                      units='days since 0001-01-01', calendar='noleap') - 1,
                        cftime.date2num(cftime.DatetimeNoLeap(year, mon, eom_day_noleap[mon-1]),
                                      units='days since 0001-01-01', calendar='noleap')]
                       for year, mon in product(years, range(1, 13))]), dims=('time', 'ntb'))