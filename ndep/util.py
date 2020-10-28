"""utility functions"""

def ds_clean(ds):
    """
    clean up, in-place, metadata in ds, and return ds
    avoid extraneous _FillValue attributes
    """
    for var in ds.variables:
        if '_FillValue' not in ds[var].encoding:
            ds[var].encoding['_FillValue'] = None
    return ds
