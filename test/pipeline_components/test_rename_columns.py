import pytest 

import pandas as pd

import sys, os
home_directory = '/home/matthew'
sys.path.append(home_directory+'/food-diary-analysis/lib')
print(sys.path)
from pipeline_components import pipeline_components as pc

def run_component(df, options={}):
    return pc.RenameColumns(df, options).run()

def test_empty_dataframe():
    input_df = pd.DataFrame({})

    result_df = run_component(input_df)

    expected_df = pd.DataFrame({})

    pd.testing.assert_frame_equal(result_df, expected_df)

def test_columns_to_rename_not_in_dataframe():
    input_df = pd.DataFrame(
        {
            'col1': [None],
            'col2': [None]
        }
    )

    with pytest.raises(ValueError) as e:
        run_component(
            input_df, 
            {
                "rename_map": {
                    'col3': 'new_col3',
                    'col4': 'new_col4'
                }
            }
        )
    
    assert str(e.value) == 'Some or all required columns [\'col3\', \'col4\'] are not found in input dataframe columns [\'col1\', \'col2\']'

def test_some_columns_to_rename_not_in_dataframe():
    input_df = pd.DataFrame(
        {
            'col1': [None],
            'col2': [None]
        }
    )

    with pytest.raises(ValueError) as e:
        run_component(
            input_df, 
            {
                "rename_map": {
                    'col2': 'new_col2',
                    'col3': 'new_col3'
                }
            }
        )
    
    assert str(e.value) == 'Some or all required columns [\'col2\', \'col3\'] are not found in input dataframe columns [\'col1\', \'col2\']'

def test_rename_multiple_columns():
    input_df = pd.DataFrame(
        {
            'col1': [None],
            'col2': [None],
            'col3': [None]
        }
    )

    result_df = run_component(
        input_df,
        {
            "rename_map": {
                'col1': 'new_col1',
                'col3': 'new_col3'
            }
        }
    )

    expected_df = pd.DataFrame(
        {
            'new_col1': [None],
            'col2': [None],
            'new_col3': [None]
        }
    )

    pd.testing.assert_frame_equal(result_df, expected_df)