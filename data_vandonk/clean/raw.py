import os
from typing import Optional
from ftplib import FTP

import pandas as pd
import xarray as xr
import requests

from econtools import load_or_build

from data_vandonk.util.env import src_path, data_path
from data_vandonk.util import _restrict_to_conus


def vandonk_monthly(year: int, month: int,
                    species: str='PM25') -> pd.DataFrame:
    netcdf = vandonk_monthly_netcdf(year, month, species)

    return netcdf


def vandonk_monthly_netcdf(year: int, month: int, species: str):
    filepath = vandonk_month_local_path(year, month, species)
    if not os.path.isfile(filepath):
        download_vandonk_monthly(filepath, year, month, species)
    netcdf = xr.open_dataset(filepath)

    return netcdf


def download_vandonk_monthly(
        filepath: str, year: int, month: int,
        species: str,
        ftp: Optional[FTP]=None) -> pd.DataFrame:

    if ftp is None:
        ftp = _setup_FTP(species)

    str_mo = str(month).zfill(2)
    remote_filename = (
        f'GWRwSPEC_PM25_NA_{year}{str_mo}_{year}{str_mo}-RH35.nc'
    )
    with open(vandonk_month_local_path(year, month, species), 'wb') as f:
        ftp.retrbinary(f'RETR {remote_filename}', f.write)

def _setup_FTP(species: str) -> FTP:
    ftp = FTP('stetson.phys.dal.ca')
    ftp.login()
    ftp.cwd(f'Aaron/V4NA02/Monthly/netcdf/{species}')

    return ftp


def vandonk_month_local_path(year: int, month: int, species: str) -> str:
    str_mo = str(month).zfill(2)
    local_path = src_path(
        'monthly',
        f'GWRwSPEC_PM25_NA_{year}{str_mo}_{year}{str_mo}-RH35.nc')
    return local_path


@load_or_build(data_path('multisat_conus_{}_{}.pkl'), path_args=[0, 'nodust'])
def multisat_conus_year(year: int, nodust: bool=False) -> pd.DataFrame:

    df = load_multisat_year(year, nodust=nodust)

    df = _restrict_to_conus(df)

    df = df.stack('x')

    return df


def load_multisat_year(year: int, nodust: bool=False) -> pd.DataFrame:
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
