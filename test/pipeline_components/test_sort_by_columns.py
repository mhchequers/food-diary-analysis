import pytest 

import pandas as pd

import sys, os
home_directory = '/home/matthew'
sys.path.append(home_directory+'/food-diary-analysis/lib')
print(sys.path)
from pipeline_components import pipeline_components as pc

def run_component(df, options={}):
    return pc.SortByColumns(df, options).run()

def test_empty_dataframe():
    input_df = pd.DataFrame({})

    with pytest.raises(IndexError) as e:
        run_component(input_df)
    
    assert str(e.value) == 'list index out of range'

def test_no_specified_columns_to_sort_by():
    input_df = pd.DataFrame(
        {
            'col1': [None],
            'col2': [None]
        }
    )

    with pytest.raises(IndexError) as e:
        run_component(input_df)
    
    assert str(e.value) == 'list index out of range'


def test_sort_by_columns_not_in_dataframe():
    input_df = pd.DataFrame(
        {
            'col1': [None],
            'col2': [None]
        }
    )

    options = {"columns_to_sort_by": ['col3', 'col4']}

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

    options = {"columns_to_sort_by": ['col2', 'col3']}

    with pytest.raises(ValueError) as e:
        run_component(input_df, options)
    
    assert str(e.value) == 'Some or all required columns [\'col2\', \'col3\'] are not found in input dataframe columns [\'col1\', \'col2\']'

def test_number_of_sort_by_columns_not_equal_to_number_of_ascending_flags():
    input_df = pd.DataFrame(
        {
            'col1': [None],
            'col2': [None],
            'col3': [None]
        }
    )

    options = {
        "columns_to_sort_by": ['col1', 'col2', 'col3'],
        "ascending_flags": [True, False]
    }

    with pytest.raises(ValueError) as e:
        run_component(input_df, options)
    
    assert str(e.value) == 'Number of columns to sort is not equal to number of ascending flags'

def test_invalid_ascending_flag_type():
    input_df = pd.DataFrame(
        {
            'col1': [None],
            'col2': [None],
            'col3': [None]
        }
    )

    options = {
        "columns_to_sort_by": ['col1', 'col2', 'col3'],
        "ascending_flags": [True, 3, "not_a_boolean"]
    }

    with pytest.raises(ValueError) as e:
        run_component(input_df, options)
    
    assert str(e.value) == 'All ascending flags must be of type boolean'

def test_sort_columns_in_dataframe():
    input_df = pd.DataFrame(
        {
            'col1': [1, 3, 2, 6, 7],
            'col2': [4, 4, 2, 2, 6],
            'col3': [2, 7, 4, 9, 3]
        }
    )

    options = {
        "columns_to_sort_by": ['col2', 'col1'],
        "ascending_flags": [True, False]
    }
    result_df = run_component(input_df, options)

    expected_df = pd.DataFrame(
        {
            'col1': [6, 2, 3, 1, 7],
            'col2': [2, 2, 4, 4, 6],
            'col3': [9, 4, 7, 2, 3]
        }
    )

    pd.testing.assert_frame_equal(result_df, expected_df)
    