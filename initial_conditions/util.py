import numpy as np
import xarray as xr
from netCDF4 import default_fillvals
import fill_POP_core

def fill_ocean_POP(da_in, mask, ltripole=False):
    '''Fill missing values on the POP grid by interative smoothing operation.'''

    non_lateral_dims = da_in.dims[:-2]

    if not non_lateral_dims:
        da_in = fill_ocean_POP_single_layer(da_in, mask, ltripole)

    elif non_lateral_dims == ('time',):
        if mask.dims != ('nlat', 'nlon'):
            raise ValueError('Mask dims do not match data')

        for l in range(da_in.shape[0]):
            da_in.values[l, :, :] = fill_ocean_POP_single_layer(da_in[l, :, :],
                                                                mask[:, :],
                                                                ltripole)

    elif non_lateral_dims == ('z_t',):
        if mask.dims != ('z_t', 'nlat', 'nlon'):
            raise ValueError('Mask dims do not match data')

        for k in range(da_in.shape[0]):
            da_in.values[k, :, :] = fill_ocean_POP_single_layer(da_in[k, :, :],
                                                                mask[k, :, :],
                                                                ltripole)
    elif non_lateral_dims == ('time', 'z_t',):
        if mask.dims != ('z_t', 'nlat', 'nlon'):
            raise ValueError('Mask dims do not match data')

        for l in range(da_in.shape[0]):
            for k in range(da_in.shape[1]):
                da_in.values[l, k, :, :] = fill_ocean_POP_single_layer(
                    da_in[l, k, :, :], mask[k, :, :],
                    ltripole)
    else:
        raise ValueError(f'Unknown dims: {non_lateral_dims}')

    return da_in


def fill_ocean_POP_single_layer(da_in, mask, ltripole=False):

    tol = 1.0e-4

    fillmask = (np.isnan(da_in) & mask).values
    if not fillmask.any():
        return da_in

    var_pass = da_in.values.astype(np.float32).T
    msv = default_fillvals['f4']
    var_pass[np.isnan(var_pass)] = msv

    add_attrs = {'note': 'fill_ocean_POP applied'}

    fill_POP_core.fill_pop_core(var=var_pass,
                                fillmask=fillmask.T,
                                msv=msv,
                                tol=tol,
                                ltripole=ltripole)

    var_pass[var_pass == msv] = np.nan

    da_out = xr.DataArray(var_pass.T.astype(da_in.dtype),
                        dims=da_in.dims,
                        coords=da_in.coords,
                        attrs=da_in.attrs.update(add_attrs))
    da_out.encoding = da_in.encoding

    return da_out