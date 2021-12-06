# Package Overview

Functions to download data from van Donkelaar et al. (2019) and similar papers
and reformat the data into pandas DataFrames.

# Using package

1. Clone (i.e., install) code.
2. The variable `DATA_PATH` in the file `data_vandonk/util/env.py` specifies
   where on your computer you want to save data files, including both raw
   downloads and intermediate files created by this code. It is currently set
   up for my computer and will point to `d:\Data\data-vandonk`; if you want
   your data to be somewhere else, you will need to change the value of
   `DATA_PATH`. You may also want to change the format of the intermediate file
   that is stored (see Step 5 below).
3. Install the `data_vandonk` python package. Inside the `data_vandonk`
   directory, run: `python setup.py install`. This may require that you install
   other packages, such as pandas and econtools.
4. Download raw files using the `batch_download_vandonk_monthly` function.
   Where these files are saved is determined by the `DATA_PATH` variable (see
   Step 2 above). 
   Specify which years you wish to download data for. See docstring (e.g.,
   `help` function in Python) for further details.
   For example, the following script will download all monthly files for PM2.5
   between 2013 and 2016:

   ```python
   from data_vandonk import batch_download_vandonk_monthly

   if __name__ == '__main__':
       start_year = 2013
       end_year = 2016
       species = 'PM25'
       df = batch_download_vandonk_monthly(start_year=start_year,
                                           end_year=end_year,
                                           species=species)
   ```

5. Convert downloaded data into usable format. The raw data are in NetCDF
   format, which is not something most applied social science researchers use.
   The function `vandonk_monthly_conus` will convert these data into a simple
   table and save that table as a file on your computer (again, determined by
   `DATA_PATH`). The default file format is a Python pickle file (`.pkl`). If
   you want to use some other format like a CSV (`.csv`) or a Stata DTA file
   (`.dta`), you can change the file extension on line 15 of file
   `data_vandonk/clean/raw.py` *before* you do the installation on Step 3. If
   you already did the installation before reading this far, you can just do it
   again after making the change. An example script is:

   ```python
   from data_vandonk import vandonk_monthly_conus

   if __name__ == '__main__':
       year = 2012
       month = 6
       species = 'PM25'
       df = vandonk_monthly_conus(year, month, species=species)
   ```


6. Use the data however you want! The function `vandonk_monthly_conus` will
   cache the reformated data to disk but will also read the cached data, so you
   can use that function directly in your analyses. You should also cite the
   original van Donkelaar et al. paper that generated these raw data and you
   may consider citing the paper for which this package was created:

   Sullivan, Daniel M. and Alan Krupnick. 2019. "Using Satellite Data to Fill
   the Gaps in the US Air Pollution Monitoring Network." Resources for the
   Future Working Paper.

   See http://www.danielmsullivan.com/pages/research.html
