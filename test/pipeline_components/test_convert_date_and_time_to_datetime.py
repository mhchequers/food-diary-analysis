import pytest 

import pandas as pd
import datetime as dt
import pytz

import sys, os
home_directory = '/home/matthew'
sys.path.append(home_directory+'/food-diary-analysis/lib')
print(sys.path)
from pipeline_components import pipeline_components as pc

def run_component(df, options={}):
    return pc.ConvertDateAndTimeToDatetime(df, options).run()

def test_empty_input_dataframe():
    input_df = pd.DataFrame({})

    with pytest.raises(ValueError) as e:
        run_component(input_df)
    
    assert str(e.value) == 'Some or all required columns [\'date\', \'time\'] are not found in input dataframe columns []'

def test_input_dataframe_with_one_missing_required_columns():
    input_df = pd.DataFrame(
        {
            'date': ['April 15 2021'],
            'not_time': ['5:00 pm'],
            'another_column': [None]
        }
    )

    with pytest.raises(ValueError) as e:
        run_component(input_df)
    
    assert str(e.value) == 'Some or all required columns [\'date\', \'time\'] are not found in input dataframe columns [\'date\', \'not_time\', \'another_column\']'

def test_input_dataframe_with_missing_required_columns():
    input_df = pd.DataFrame(
        {
            'column': [1]
        }
    )

    with pytest.raises(ValueError) as e:
        run_component(input_df)
    
    assert str(e.value) == 'Some or all required columns [\'date\', \'time\'] are not found in input dataframe columns [\'column\']'

def test_input_dataframe_with_default_timezone():
    input_df = pd.DataFrame(
        {
            'date': ['April 15 2021', 'April 16 2021'],
            'time': ['5:00 pm', '5:00 am']
        }
    )

    result_df = run_component(input_df)

    timezone = pytz.timezone('US/Eastern')
    expected_df = input_df = pd.DataFrame(
        {
            'date': ['April 15 2021', 'April 16 2021'],
            'time': ['5:00 pm', '5:00 am'],
            'datetime': [
                timezone.localize(dt.datetime(2021, 4, 15, 17, 0)),
                timezone.localize(dt.datetime(2021, 4, 16, 5, 0))
            ]
        }
    )

    pd.testing.assert_frame_equal(result_df, expected_df)

def test_input_dataframe_with_optional_timezone():
    input_df = pd.DataFrame(
        {
            'date': ['April 15 2021', 'April 16 2021'],
            'time': ['5:00 pm', '5:00 am']
        }
    )

    result_df = run_component(input_df, {"timezone": 'US/Pacific'})

    timezone = pytz.timezone('US/Pacific')
    expected_df = input_df = pd.DataFrame(
        {
            'date': ['April 15 2021', 'April 16 2021'],
            'time': ['5:00 pm', '5:00 am'],
            'datetime': [
                timezone.localize(dt.datetime(2021, 4, 15, 17, 0)),
                timezone.localize(dt.datetime(2021, 4, 16, 5, 0))
            ]
        }
    )

    pd.testing.assert_frame_equal(result_df, expected_df)