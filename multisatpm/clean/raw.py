import pandas as pd
import xarray as xr

from multisatpm.util.env import src_path

# data: http://fizz.phys.dal.ca/~atmos/martin/?page_id=140

# 1998-2007
nc_filepath_1 = 'GlobalGWRwUni_PM25_GL_{}01_{}12-RH35_Median_NoDust_NoSalt.nc'

# 2008-2016
nc_filepath_2 = 'GlobalGWR_PM25_GL_{}01_{}12-RH35_NoDust_NoSalt.nc'

years_1 = range(1998, 2008)
years_2 = range(2008, 2017)


def load_multisatpm():
    nc_file = xr.open_dataset(src_path(nc_filepath_1.format(1998, 1998)))
    df = nc_file.to_dataframe()

    df = pd.DataFrame(nc_file['PM25'].data)
    df.index = nc_file['LAT'].data
    df.columns = nc_file['LON'].data

    df.index.name = 'y'
    df.columns.name = 'x'

    # Restrict to CONUS
    x0 = -124.7844079
    x1 = -66.9513812
    y0 = 24.7433195
    y1 = 49.3457868
    df_conus = df.loc[y1:y0, x0:x1]

    df_conus = df_conus.stack('x')

    return df_conus


if __name__ == '__main__':
    df = load_multisatpm()


# WIP loop through all multisat data


def multisat_loop_trial1():  # XXX can't convert list to df
    nc_files = [xr.open_dataset(src_path(nc_filepath_1.format(year, year))) for year in years_1]

    df = nc_files.to_dataframe()

    df = pd.DataFrame(nc_files['PM25'].data)
    df.index = nc_files['LAT'].data
    df.columns = nc_files['LON'].data

    df.index.name = 'y'
    df.columns.name = 'x'

    x0 = -124.7844079
    x1 = -66.9513812
    y0 = 24.7433195
    y1 = 49.3457868
    df_conus = df.loc[y1:y0, x0:x1]

    df_conus = df_conus.stack('x')
    df = pd.concat(df_conus)

    del df_conus

    return df


def multisat_loop_trial2():
    for year in years_1:
        nc_files = xr.open_dataset(src_path(nc_filepath_1.format(year, year)))
        df = nc_files.to_dataframe()

        df = pd.DataFrame(nc_files['PM25'].data)
        df.index = nc_files['LAT'].data
        df.columns = nc_files['LON'].data

        df.index.name = 'y'
        df.columns.name = 'x'

        x0 = -124.7844079
        x1 = -66.9513812
        y0 = 24.7433195
        y1 = 49.3457868
        df_conus = df.loc[y1:y0, x0:x1]

        df_conus = df_conus.stack('x')

        if(year == 1998):
            df = df_conus
        else:
            df = df.append(df_conus)

    return df
