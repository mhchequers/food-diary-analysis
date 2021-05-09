import pytest 

import pandas as pd

import sys, os
home_directory = '/home/matthew'
sys.path.append(home_directory+'/food-diary-analysis/lib')
print(sys.path)
from pipeline_components import pipeline_components as pc

def run_component(df, options={}):
    return pc.ConvertStringColumnToListOfStrings(df, options).run()

def test_empty_dataframe():
    input_df = pd.DataFrame({})

    with pytest.raises(ValueError) as e:
        run_component(input_df)
    
    assert str(e.value) == 'Some or all required columns [\'\'] are not found in input dataframe columns []'

def test_dataframe_with_missing_required_column():
    input_df = pd.DataFrame(
        {
            'col1': [None],
            'col2': [None],
        }
    )

    with pytest.raises(ValueError) as e:
        run_component(input_df, {"column_to_convert": "not_a_col"})
    
    assert str(e.value) == 'Some or all required columns [\'not_a_col\'] are not found in input dataframe columns [\'col1\', \'col2\']'

def test_dataframe_with_default_required_column():
    input_df = pd.DataFrame(
        {
            'col1': [None],
            'col2': [None],
        }
    )

    with pytest.raises(ValueError) as e:
        run_component(input_df)
    
    assert str(e.value) == 'Some or all required columns [\'\'] are not found in input dataframe columns [\'col1\', \'col2\']'

def test_wrong_dtype_of_column():
    input_df = pd.DataFrame(
        {
            'col': [4]
        }
    )

    with pytest.raises(ValueError) as e:
        run_component(input_df, {"column_to_convert": "col"})
    
    assert str(e.value) == 'Column to convert col is not of dtype Object, but is of type int64'
    

def test_input_dataframe_with_default_separater():
    input_df = pd.DataFrame(
        {
            'col': ['this, is, a, bunch, of, strings', 'another, bunch, of, strings']
        }
    )

    result_df = run_component(input_df, {"column_to_convert": "col"})

    expected_df = pd.DataFrame(
        {
            'col': [['this', 'is', 'a', 'bunch', 'of', 'strings'], ['another', 'bunch', 'of', 'strings']]
        }
    )

    pd.testing.assert_frame_equal(result_df, expected_df)