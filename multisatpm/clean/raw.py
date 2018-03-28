import xarray as xr

from util.env import src_path

ds = xr.open_dataset('M:/EPA_AirPollution/Data/multisatpm/src/GlobalGWR_PM25_GL_200801_200812-RH35_NoDust_NoSalt.nc')
df = ds.to_dataframe()

df.index
