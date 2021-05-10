import pytest 

import pandas as pd
import math

import sys, os
home_directory = '/home/matthew'
sys.path.append(home_directory+'/food-diary-analysis/lib')
print(sys.path)
from pipeline_components import pipeline_components as pc

def run_component(df, options={}):
    return pc.CalculateMeanAndStdDevOfColumn(df, options).run()

def test_empty_dataframe_with_default_options():
    input_df = pd.DataFrame({})

    with pytest.raises(ValueError) as e:
        run_component(input_df)
    
    assert str(e.value) == 'Some or all required columns [\'\'] are not found in input dataframe columns []'


def test_partially_invalid_columns_to_groupby_and_default_invalid_column_to_aggregate():
    input_df = pd.DataFrame(
        {
            'col1': [None],
            'col2': [None],
            'col3': [None]
        }
    )

    with pytest.raises(ValueError) as e:
        run_component(
            input_df, 
            {
                "columns_to_groupby": ['col3', 'col4']
            }
        )
    
    assert str(e.value) == 'Some or all required columns [\'col3\', \'col4\', \'\'] are not found in input dataframe columns [\'col1\', \'col2\', \'col3\']'

def test_partially_invalid_columns_to_groupby_and_valid_column_to_aggregate():
    input_df = pd.DataFrame(
        {
            'col1': [None],
            'col2': [None],
            'col3': [None]
        }
    )

    with pytest.raises(ValueError) as e:
        run_component(
            input_df, 
            {
                "columns_to_groupby": ['col3', 'col4'],
                "column_to_aggregate": "col3"
            }
        )
    
    assert str(e.value) == 'Some or all required columns [\'col3\', \'col4\', \'col3\'] are not found in input dataframe columns [\'col1\', \'col2\', \'col3\']'


def test_invalid_col_to_aggregate_with_default_columns_to_groupby():
    input_df = pd.DataFrame(
        {
            'col1': [None],
            'col2': [None],
            'col3': [None]
        }
    )

    with pytest.raises(ValueError) as e:
        run_component(
            input_df, 
            {
                "column_to_aggregate": "not_a_column"
            }
        )
    
    assert str(e.value) == 'Some or all required columns [\'not_a_column\'] are not found in input dataframe columns [\'col1\', \'col2\', \'col3\']'

def test_invalid_col_to_aggregate_with_with_valid_columns_to_groupby():
    input_df = pd.DataFrame(
        {
            'col1': [None],
            'col2': [None],
            'col3': [None]
        }
    )

    with pytest.raises(ValueError) as e:
        run_component(
            input_df, 
            {
                "columns_to_groupby": ['col1', 'col2'],
                "column_to_aggregate": "not_a_column"
            }
        )
    
    assert str(e.value) == 'Some or all required columns [\'col1\', \'col2\', \'not_a_column\'] are not found in input dataframe columns [\'col1\', \'col2\', \'col3\']'

def test_invalid_columns_to_groupby_and_invalid_column_to_aggregate():
    input_df = pd.DataFrame(
        {
            'col1': [None],
            'col2': [None],
            'col3': [None]
        }
    )

    with pytest.raises(ValueError) as e:
        run_component(
            input_df, 
            {
                "columns_to_groupby": ['col4', 'col5'],
                "column_to_aggregate": "not_a_column"
            }
        )
    
    assert str(e.value) == 'Some or all required columns [\'col4\', \'col5\', \'not_a_column\'] are not found in input dataframe columns [\'col1\', \'col2\', \'col3\']'

def test_column_to_aggregate_in_columns_to_groupby():
    input_df = pd.DataFrame(
        {
            'col1': [None],
            'col2': [None],
            'col3': [None]
        }
    )

    with pytest.raises(ValueError) as e:
        run_component(
            input_df, 
            {
                "columns_to_groupby": ['col1', 'col2'],
                "column_to_aggregate": "col2"
            }
        )
    
    assert str(e.value) == 'Column to aggregate cannot be in columns to groupby'

def test_groupby_single_column():
    input_df = pd.DataFrame(
        {
            'col1': ["cat", "dog", "cat", "dog"],
            'col2': [1, 2, 3, 4]
        }
    )

    result_df = run_component(
        input_df,
        {
            "columns_to_groupby": ['col1'],
            "column_to_aggregate": "col2"
        }
    )

    expected_df = pd.DataFrame(
        {
            'col1': ["cat", "dog"],
            'col2_mean': [2, 3],
            'col2_std': [1.414214, 1.414214],
            'col2_count': [2, 2]
        }
    )

    pd.testing.assert_frame_equal(result_df, expected_df)

def test_groupby_single_column_with_single_count_aggregate():
    input_df = pd.DataFrame(
        {
            'col1': ["cat", "dog", "dog"],
            'col2': [1, 2, 4]
        }
    )

    result_df = run_component(
        input_df,
        {
            "columns_to_groupby": ['col1'],
            "column_to_aggregate": "col2"
        }
    )

    expected_df = pd.DataFrame(
        {
            'col1': ["cat", "dog"],
            'col2_mean': [1, 3],
            'col2_std': [math.nan, 1.414214],
            'col2_count': [1, 2]
        }
    )

    pd.testing.assert_frame_equal(result_df, expected_df)

def test_groupby_multiple_columns():
    input_df = pd.DataFrame(
        {
            'col1': ["cat", "dog", "cat", "dog"],
            'col2': [1, 2, 3, 4],
            'col3': ["lucy", "frank", "gizmo", "frank"]
        }
    )

    result_df = run_component(
        input_df,
        {
            "columns_to_groupby": ['col3', 'col1'],
            "column_to_aggregate": "col2"
        }
    )

    expected_df = pd.DataFrame(
        {
            'col3': ["frank", "gizmo", "lucy"],
            'col1': ["dog", "cat", "cat"],
            'col2_mean': [3, 3, 1],
            'col2_std': [1.414214, math.nan, math.nan],
            'col2_count': [2, 1, 1]
        }
    )

    pd.testing.assert_frame_equal(result_df, expected_df)