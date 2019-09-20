# Package Overview

Functions to download data from van Donkelaar et al. (2019) and similar papers
and reformat the data into pandas DataFrames.

# Primary Methods

- `mass_download_vandonk_monthly`. Downloads all files for North
   American-calibrated data for the given time period and species.

- `vandonk_monthly_conus`. Returns a DataFrame for the given year, month, and
   pollution species. Data are from the data product calibrated to North
   America and then restructed to the continental United States (CONUS).

   **Example:**

   ```python
   from data_vandonk import vandonk_monthly_conus
   
   if __name__ == '__main__':
       year = 2012
       month = 6
       species = 'PM25'
       df = vandonk_monthly_conus(year, month, species=species)
   ```
