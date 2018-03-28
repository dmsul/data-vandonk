import xarray as xr

from multisatpm.util.env import src_path

nc_file = xr.open_dataset(src_path(
        'GlobalGWR_PM25_GL_200801_200812-RH35_NoDust_NoSalt.nc')
        )

df = nc_file.to_dataframe()

df.index
