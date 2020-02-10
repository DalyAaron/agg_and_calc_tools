# Data Aggregation and Calculation Assignment

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

## Running the Tests

The testing script is named tests.py it contains tests that will output on the command line if there are any failures or success. To run:
```
$ python3 tests.py
```
