# Data Aggregation and Calculation Module

This is a module which cleans and aggregates a time-series financial dataset and performs calculations including:

* End of Day Capital
* Begin of Day Capital
* Daily Return

## Getting Started

The repository contains the module file - agg_calc_tools.py This file can be imported to your script using:
```
import agg_calc_tools as act
```

The repository also contains an example dataset named practical.csv and a testing file named tests.py

### Prerequisites

This module requires installation of Pandas and DateParser. Examples of how to install are below:
```
$ pip install pandas
```
```
$ pip install dateparser
```

## Module functions

Here is a list of the modules functions:

#### agg_calc_tools.read_csv(filepath: str)
Reads in a specified csv from the filepath variable, cleanses the data and returns a pandas.DataFrame.

#### agg_calc_tools.aggregate_by_date(df: pd.DataFrame)
Takes a pandas.DataFrame as the argument. Groups the data on unique_id by date, aggregates by summing numerical columns and using the alphabetical first for string columns. Returns a pandas.DataFrame.

#### agg_calc_tools.get_eod_capital(df_agg: pd.DataFrame)
Takes the aggregated pandas.DataFrame returned from aggregate_by_date and calculates end of day capital. Returns a pandas.DataFrame containing eod_capital for each day.

#### agg_calc_tools.get_bod_capital(df_eod: pd.DataFrame)
Takes the pandas.DataFrame returned from get_eod_capital and calculates begin of day capital. Returns a pandas.DataFrame containing bod_capital for each day.

#### agg_calc_tools.merge_eod_bod(df_agg: pd.DataFrame, df_eod: pd.DataFrame, df_bod: pd.DataFrame)
Takes three pandas.DataFrame objects, aggregated, eod, and bod and merges together on common dates. Returns a pandas.DataFrame containing aggregated data and eod_capital and bod_capital columns.

#### agg_calc_tools.daily_return(df_merged: pd.DataFrame)
Takes the merged pandas.DataFrame from merge_eod_bod and calculates the daily return for each security. Returns a pandas.DataFrame containing daily_return column.

#### agg_calc_tools.write_to_csv(df_out: pd.DataFrame, filepath: str)
Takes two arguments, a pandas.DataFrame object to be outputted to a csv and a filepath string specifying location and name of file to be outputed to.

## Running the Tests

The testing script is named tests.py it contains tests that will output on the command line if there are any failures or success. To run:
```
$ python3 tests.py
```
After running tests, the output can be viewed in the out.csv file. This will contain the final aggregated and calculated data.

## Author

* **Aaron Daly**
