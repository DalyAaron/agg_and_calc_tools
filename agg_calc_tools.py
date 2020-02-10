#!/usr/bin/env python
import pandas as pd
import dateparser

def read_csv(filepath: str) -> pd.DataFrame:
    # check input type is correct
    if not isinstance(filepath, str):
        raise TypeError("Argument must be of type str")
    # check the filepath is correct and try to read in file to dataframe
    if not filepath.endswith('.csv'):
        filepath = filepath + '.csv'
    try:
        df = pd.read_csv(filepath)
    except:
        raise FileNotFoundError('Filepath must be a valid .csv file')
    # start pre-processing and cleaning of dataframe
    # fill date if not already 8 chars
    df.date = df.date.astype(str).str.zfill(8)
    # apply dateparser to each date in df.date
    df.date = df.date.apply(lambda x : dateparser.parse(str(x), date_formats=['%d%m%Y','%Y%m%d']))
    return df

def aggregate_by_date(df: pd.DataFrame) -> pd.DataFrame:
    # check input type is correct
    if not isinstance(df, pd.DataFrame):
        raise TypeError("Argument must be of type pandas.DataFrame")
    # aggregate by date and id summing numeric cols and sorting alphabetically any string cols
    df_agg = df.groupby(['date','id']).agg(lambda x : x.min() if x.dtype=='object' else x.sum())
    # replace Technology with Information Technology
    df_agg.loc[(df_agg.sector == 'Technology'),'sector'] = 'Information Technology'
    return df_agg

def get_eod_capital(df_agg: pd.DataFrame) -> pd.DataFrame:
    # check input type is correct
    if not isinstance(df_agg, pd.DataFrame):
        raise TypeError("Argument must be of type pandas.DataFrame")
    # sum the total exposure for all securities for the day
    df_eod = df_agg[['exposure','pal']].groupby(level='date').sum()
    df_eod.rename(columns={'exposure':'eod_capital', 'pal':'total_pal'}, inplace = True)
    return df_eod

def get_bod_capital(df_eod: pd.DataFrame) -> pd.DataFrame:
    # check input type is correct
    if not isinstance(df_eod, pd.DataFrame):
        raise TypeError("Argument must be of type pandas.DataFrame")
    # get the end of day capital for the previous day
    s_bod = df_eod.eod_capital.shift(1)
    # for first day subtract the total P&L from total exposure for the day
    s_bod[0] = df_eod.eod_capital[0] - df_eod.total_pal[0]
    df_bod = s_bod.to_frame()
    df_bod.rename(columns={'eod_capital':'bod_capital'}, inplace = True)
    return df_bod

def merge_eod_bod(df_agg: pd.DataFrame, df_eod: pd.DataFrame, df_bod: pd.DataFrame) -> pd.DataFrame:
    # check input type is correct
    if not isinstance(df_agg, pd.DataFrame) or not isinstance(df_eod, pd.DataFrame) or not isinstance(df_bod, pd.DataFrame):
        raise TypeError("Arguments must be of type pandas.DataFrame")
    # merge eod and bod on df_aggs group index
    df_merged = pd.merge(df_agg, df_eod, left_index = True, right_index = True)
    df_merged = pd.merge(df_merged, df_bod, left_index = True, right_index = True)
    return df_merged

def daily_return(df_merged: pd.DataFrame) -> pd.DataFrame:
    # check input type is correct
    if not isinstance(df_merged, pd.DataFrame):
        raise TypeError("Argument must be of type pandas.DataFrame")
    # create daily_return column from pal / bod_capital
    df_merged['daily_return'] = df_merged.pal / df_merged.bod_capital
    return df_merged

def write_to_csv(df_out: pd.DataFrame, filepath: str):
    # check input type is correct
    if not isinstance(df_out, pd.DataFrame) or not isinstance(filepath, str):
        raise TypeError("First argument must be of type pandas.DataFrame, second argument must be of type str")
    # check filepath ends with csv, and append if not
    if not filepath.endswith(".csv"):
        filepath = filepath + ".csv"
    df_out.to_csv(filepath)
