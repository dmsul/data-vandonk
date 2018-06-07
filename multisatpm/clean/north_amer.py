import os
import zipfile
from urllib.request import urlretrieve

import numpy as np
import pandas as pd
import xarray as xr

from econtools import load_or_build

from multisatpm.util.env import src_path, data_path
from multisatpm.util import _restrict_to_conus

file_format = 'GWRwSPEC_PM25_NA_{0}01_{0}12-RH35.nc'


@load_or_build(data_path('northamer_1year_{}.pkl'), path_args=[0])
def msat_northamer_1year(year):
    df = msat_northamer_1year_to_df(year)
    df = _restrict_to_conus(df)
    df = df.stack('x')

    return df


def msat_northamer_1year_to_df(year: int) -> pd.DataFrame:
    filepath = src_path(file_format.format(year))
    if not os.path.isfile(filepath):
        msat_northamer_1year_download(year)

    netcdf = xr.open_dataset(filepath)
    df = pd.DataFrame(netcdf['PM25'].data)
    df.index = netcdf['LAT'].data
    df.columns = netcdf['LON'].data

    df.index.name = 'y'
    df.columns.name = 'x'

    return df


def msat_northamer_1year_download(year):
    url_root = 'ftp://stetson.phys.dal.ca/Aaron/ForDaniel/'
    filename = file_format.format(year)
    url = url_root + filename

    print(f"Downloading msat NA 1year {year}...", end='')
    urlretrieve(url, filename=src_path(filename))
    print("Done.")


@load_or_build(data_path('northamer_3year_{}.pkl'), path_args=[0])
def msat_northamer_conus_3year(yearT):
    df = msat_northamer_3year(yearT)

    df = _restrict_to_conus(df)

    df = df.stack('x', dropna=False)

    df = df.astype(np.float32)

    df.name = 'pm25'

    return df


def msat_northamer_3year(yearT):
    year0 = yearT - 2
    meta_rows = 6
    file_path = src_path('GWR_PM25_NA_{}01_{}12-RH35-NoNegs.asc')
    file_path = file_path.format(year0, yearT)

    # Unzip if needed
    if not os.path.isfile(file_path):
        print(f"Unzipping {yearT}")
        zip_ref = zipfile.ZipFile(file_path + '.zip', mode='r')
        file_split = os.path.split(file_path)
        zip_ref.extract(file_split[1], path=file_split[0])
        zip_ref.close()

    # Extract metadata
    meta = pd.read_table(file_path,
                         nrows=meta_rows,
                         sep='\s+',
                         header=None)
    meta = meta.set_index(0).squeeze()

    # Extract main data
    df = pd.read_table(file_path,
                       skiprows=meta_rows,
                       sep='\s+',
                       header=None)

    # Construct geo coords from metadata
    cellsize = meta['cellsize']

    ymin = meta['yllcenter']
    ymax = ymin + cellsize * (meta['nrows'] - 1)
    index = np.arange(ymax, ymin, -1 * cellsize)
    df.index = index

    xmin = meta['xllcenter']
    xmax = xmin + cellsize * (meta['ncols'] - 1)
    cols = np.arange(xmin, xmax + cellsize, cellsize)
    df.columns = cols

    df.index.name = 'y'
    df.columns.name = 'x'

    # Re-code missings # NOTE: 'NODATA_value' is wrong sometimes
    df[df < -1] = np.nan

    assert (df.min().min() >= 0)

    return df


if __name__ == '__main__':
    for y in range(2002, 2016):
        df = msat_northamer_1year(y)
