#!/usr/bin/env python
'''
Testing script to run unit tests on agg_calc_tools.py
'''
import unittest
import os.path
import agg_calc_tools as act

class TestSum(unittest.TestCase):
    # Test Variables
    df = act.read_csv('practical.csv')
    df_agg = act.aggregate_by_date(df)
    df_eod = act.get_eod_capital(df_agg)
    df_bod = act.get_bod_capital(df_eod)
    df_merged = act.merge_eod_bod(df_agg,df_eod,df_bod)
    df_out = act.daily_return(df_merged)

    # Test cases
    # check if file can be read with correct input
    def test_read_correct(self):
        df = act.read_csv('practical.csv')
    # check if file can be read with dropped .csv input
    def test_read_drop(self):
        df = act.read_csv('practical')
    # check if throws exception with incorrect input
    def test_read_incorrect(self):
        self.assertRaises(FileNotFoundError, act.read_csv, 'prctival.csv')
    # check if incorrect date is parsed correctly
    def test_parse_date(self):
        self.assertEqual(len(self.df[self.df['date'] == '2018-02-02']), 4, "Should be 4 records for 2018-02-02")

    # check string columns are alphabetically sorted
    def test_sorted_alpha(self):
        self.assertEqual(self.df_agg.analyst[0], 'Alice', "Alphabetically sorted should be Alice")
    # check that the columns are summed correctly
    def test_sum_col(self):
        self.assertEqual(self.df_agg.pal[0], 118700+87600, "Sum of Citigroup pal for day 1 should be 206300")
    # check if Information Technology has replaced Technology
    def test_info_repl(self):
        self.assertEqual(self.df_agg.sector.value_counts()['Information Technology'], self.df.sector.value_counts()['Technology'], "There should be an equal count")

    # check if eod_capital is calculated correctly
    def test_eod_capital(self):
        self.assertEqual(self.df_eod.eod_capital[0], 2374000+1752000+3976666.667+3154166.667, "Eod Capital for day 1 should be 11256833.334")

    # check if bod_capital is calculated correctly
    def test_bod_capital(self):
        self.assertEqual(self.df_bod.bod_capital[1], self.df_eod.eod_capital[0], "Bod Capital for day 2 should be 11256833.334")

    # check if bod_capital for first day is calculated correctly
    def test_bod_capital_first(self):
        self.assertEqual(self.df_bod.bod_capital[0], 10433433.333999999, "Bod Capital for day 1 should be total exposure - total P&L = 10433433.333999999")

    # check if eod and bod columns are in the dataframe
    def test_columns_merged(self):
        self.assertEqual(('eod_capital' in self.df_merged.columns) and ('bod_capital' in self.df_merged.columns), True, "df_merged columns should contain eod_capital and bod_capital")

    # check if daily return column is calculated correctly
    def test_daily_return(self):
        self.assertEqual(self.df_out.daily_return[0], 0.019772973420716548, "Daily return should for day 1 should be P&L / bod capital = 0.019772973420716548")

    # check if output csv is present in filesystem
    def test_file_out(self):
        act.write_to_csv(self.df_out,"out.csv")
        self.assertEqual(os.path.isfile('out.csv'), True, "out.csv should be in filepath")

    # check if function appends .csv and writes to output
    def test_file_out(self):
        act.write_to_csv(self.df_out,"out")
        self.assertEqual(os.path.isfile('out.csv'), True, "out.csv should be in filepath")

    # check if functions return error with wrong input
    def test_input_func(self):
        self.assertRaises(TypeError, act.read_csv, 123)
        self.assertRaises(TypeError, act.aggregate_by_date, 'string input')
        self.assertRaises(TypeError, act.get_eod_capital, 'string input')
        self.assertRaises(TypeError, act.get_bod_capital, 'string input')
        self.assertRaises(TypeError, act.merge_eod_bod, 'string input')
        self.assertRaises(TypeError, act.daily_return, 'string input')
        self.assertRaises(TypeError, act.write_to_csv, 123)

if __name__ == '__main__':
    unittest.main()
