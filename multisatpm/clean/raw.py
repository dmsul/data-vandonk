import pandas as pd
import xarray as xr

from econtools import load_or_build

from multisatpm.util.env import src_path, data_path
from multisatpm.util import _restrict_to_conus


@load_or_build(data_path('multisat_conus_{}_{}.pkl'), path_args=[0, 'nodust'])
def multisat_conus_year(year, nodust=False):

    df = load_multisat_year(year, nodust=nodust)

    df = _restrict_to_conus(df)

    df = df.stack('x')

    return df


def load_multisat_year(year, nodust=False):
    """ data src: http://fizz.phys.dal.ca/~atmos/martin/?page_id=140 """
    if year in tuple(range(1998, 2008)):
        filepath = (f'GlobalGWRwUni_PM25_GL_{year}01_{year}'
                    '12-RH35_Median_NoDust_NoSalt.nc')
    elif year in tuple(range(2008, 2017)):
        filepath = (f'GlobalGWR_PM25_GL_{year}01_{year}'
                    '12-RH35_NoDust_NoSalt.nc')
    else:
        raise ValueError(f"Incorrect `year` {year}")

    if not nodust:
        filepath = filepath.replace('_NoDust_NoSalt', '')

    filepath = src_path(filepath)

    netcdf = xr.open_dataset(filepath)
    df = pd.DataFrame(netcdf['PM25'].data)
    df.index = netcdf['LAT'].data
    df.columns = netcdf['LON'].data

    df.index.name = 'y'
    df.columns.name = 'x'

    return df


if __name__ == '__main__':
    pass
