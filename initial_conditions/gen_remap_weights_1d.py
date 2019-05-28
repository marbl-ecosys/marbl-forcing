import cf_units
import numpy as np
import xarray as xr
from scipy.sparse import csr_matrix

def interval_overlap(interval_1, interval_2):
    '''
    compute how much overlap there is between two intervals
    
    intervals can be tuples, lists, numpy arrays
    intervals can be specified in an increasing or decreasing order
    '''
    overlap = min([max(interval_1), max(interval_2)]) - max([min(interval_1), min(interval_2)])
    return max([0.0, overlap])
    

def gen_remap_weights_1d(src_bnds, dst_bnds, src_units='m', dst_units='m'):
    '''
    generate weights to remap from 1d src axis to 1d dst axis
    
    axes are represented as interval bounds, provided in a 2D xarray DataArray
    
    weights are returned as a scipy.sparse matrix
    '''

    src_units_obj = cf_units.Unit(src_units)
    dst_units_obj = cf_units.Unit(dst_units)
    src_len = src_bnds.shape[0]
    dst_len = dst_bnds.shape[0]
    weights_dense = np.zeros((dst_len, src_len))
    for src_ind in range(src_len):
        src_values_dst_units = src_units_obj.convert(src_bnds[src_ind, :].values, dst_units_obj)
        for dst_ind in range(dst_len):
            weights_dense[dst_ind, src_ind] = \
                interval_overlap(src_values_dst_units, dst_bnds[dst_ind, :].values)

    # normalize rows to have sum 1.0
    for dst_ind in range(dst_len):
        row_sum = weights_dense[dst_ind, :].sum()
        if row_sum > 0.0:
            weights_dense[dst_ind, :] /= row_sum

    return csr_matrix(weights_dense)