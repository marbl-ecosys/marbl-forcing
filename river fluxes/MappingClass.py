import numpy as np
from scipy.sparse import csc_matrix
import xarray as xr

class ESMFMappingWrapper(object):
    def __init__(self, ESMF_mapping_file_name):
        self._ds_map = xr.open_dataset(ESMF_mapping_file_name)
        self._src_grid_size = np.prod(self._ds_map['src_grid_dims'].data)
        self._src_grid_shape = (self._ds_map['src_grid_dims'].data[1], self._ds_map['src_grid_dims'].data[0])
        self._dst_grid_size = np.prod(self._ds_map['dst_grid_dims'].data)
        self._dst_grid_shape = (self._ds_map['dst_grid_dims'].data[1], self._ds_map['dst_grid_dims'].data[0])
        self._mapping_weights_sparse = csc_matrix((self._ds_map['S'].data,
                                                  (self._ds_map['row'].data-1, self._ds_map['col'].data-1)),
                                                  shape=(self._dst_grid_size, self._src_grid_size))

    ##################

    def map_var(self, ds_src, var_name, scale_factor=0.01):
        da_list = []
        for time in range(len(ds_src['time'])):
            native_values = ds_src[var_name].isel(time=time).data.reshape(self._src_grid_size)
            mapped_values = self._mapping_weights_sparse*(scale_factor*native_values)
            da_list.append(xr.DataArray(mapped_values.reshape(self._dst_grid_shape), dims=('y', 'x'), name=var_name))
            if var_name in ['din_riv_flux', 'don_riv_flux']:
                conv_factor = 28*1e-15*86400*365 # 28 mg / mmol, 1e-15 Tg / mg, 86400 s/d, 365 d/yr
            elif var_name in ['dic_riv_flux', 'doc_riv_flux']:
                conv_factor = 12*1e-18*86400*365 # 28 mg / mmol, 1e-18 Pg / mg, 86400 s/d, 365 d/yr
            elif var_name in ['dip_riv_flux', 'dop_riv_flux', 'dsi_riv_flux']:
                conv_factor = 1e-15*86400*365 # 1e-15 Tmol / mmol, 86400 s/d, 365 d/yr
            elif var_name in ['dfe_riv_flux']:
                conv_factor = 1e-12*86400*365 # 1e-12 Gmol / mmol, 86400 s/d, 365 d/yr
            elif var_name in ['alk_riv_flux']:
                continue
            else:
                conv_factor = 0
            self._compute_global_integral(native_values, mapped_values, conv_factor, var_name, print_stat=time in [0, len(ds_src['time'])-1])
        da = xr.concat(da_list, dim='time').assign_coords({'time': ds_src['time'].data})
        da.attrs = ds_src[var_name].attrs
        da.attrs['units'] = 'mmol/m^2/s'
        da.encoding['_FillValue'] = None
        return da
    
    ##################

    def _compute_global_integral(self, native_values, mapped_values, conv_factor, var, print_stat=False):
        r = 6371220 # radius of earth in m
        native_area = r*r*self._ds_map['area_a'].data # r^2 since area is rad^2 not m^2
        mapped_area = r*r*self._ds_map['area_b'].data # r^2 since area is rad^2 not m^2
        if print_stat:
            global_sum_native = np.sum(native_values*native_area*(0.01*conv_factor)) # 0.01 nmol/cm^2 -> mmol/m^2
            global_sum_mapped = np.sum(mapped_values*mapped_area*conv_factor)
            rel_err = np.abs((global_sum_native-global_sum_mapped)/global_sum_native)
            print(f'{var} stats: sums are {global_sum_native:.3e} (native) and {global_sum_mapped:.3e} (mapped); rel_err is {rel_err:.3e}')