import pandas as pd
import xarray as xr

from econtools import load_or_build

from multisatpm.util.env import src_path, data_path


@load_or_build(data_path('multisat_conus_{}.pkl'), path_args=[0])
def multisat_conus_year(year):

    df = load_multisat_year(year)

    # Restrict to CONUS
    x0 = -124.7844079
    x1 = -66.9513812
    y0 = 24.7433195
    y1 = 49.3457868
    df_conus = df.loc[y1:y0, x0:x1]

    df_conus = df_conus.stack('x')

    return df_conus


def load_multisat_year(year):
    """ data src: http://fizz.phys.dal.ca/~atmos/martin/?page_id=140 """
    if year in tuple(range(1998, 2008)):
        filepath = (f'GlobalGWRwUni_PM25_GL_{year}01_{year}'
                    '12-RH35_Median_NoDust_NoSalt.nc')
    elif year in tuple(range(2008, 2017)):
        filepath = (f'GlobalGWR_PM25_GL_{year}01_{year}'
                    '12-RH35_NoDust_NoSalt.nc')
    else:
        raise ValueError(f"Incorrect `year` {year}")

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
