import pytest 

import pandas as pd

import sys, os
home_directory = '/home/matthew'
sys.path.append(home_directory+'/food-diary-analysis/lib')
print(sys.path)
from pipeline_components import pipeline_components as pc

def run_component(df, options={}):
    return pc.DropColumns(df, options).run()

def test_empty_dataframe():
    input_df = pd.DataFrame({})

    result_df = run_component(input_df)

    expected_df = pd.DataFrame({})

    pd.testing.assert_frame_equal(result_df, expected_df)

def test_no_specified_columns_to_drop():
    input_df = pd.DataFrame(
        {
            'col1': [None],
            'col2': [None]
        }
    )

    result_df = run_component(input_df)

    expected_df = pd.DataFrame(
        {
            'col1': [None],
            'col2': [None]
        }
    )

    pd.testing.assert_frame_equal(result_df, expected_df)

def test_specified_columns_not_in_dateframe():
    input_df = pd.DataFrame(
        {
            'col1': [None],
            'col2': [None]
        }
    )

    options = {"columns_to_drop": ['col3', 'col4']}

    with pytest.raises(ValueError) as e:
        run_component(input_df, options)
    
    assert str(e.value) == 'Some or all required columns [\'col3\', \'col4\'] are not found in input dataframe columns [\'col1\', \'col2\']'

def test_some_specified_columns_not_in_dateframe():
    input_df = pd.DataFrame(
        {
            'col1': [None],
            'col2': [None]
        }
    )

    options = {"columns_to_drop": ['col2', 'col3']}

    with pytest.raises(ValueError) as e:
        run_component(input_df, options)
    
    assert str(e.value) == 'Some or all required columns [\'col2\', \'col3\'] are not found in input dataframe columns [\'col1\', \'col2\']'

def test_drop_columns_from_dataframe():
    input_df = pd.DataFrame(
        {
            'col1': [None],
            'col2': [None],
            'col3': [None]
        }
    )

    options = {"columns_to_drop": ['col2', 'col3']}
    result_df = run_component(input_df, options)

    expected_df = pd.DataFrame(
        {
            'col1': [None]
        }
    )

    pd.testing.assert_frame_equal(result_df, expected_df)