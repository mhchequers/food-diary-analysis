import pytest 

import pandas as pd

import sys, os
home_directory = '/home/matthew'
sys.path.append(home_directory+'/food-diary-analysis/lib')
print(sys.path)
from pipelines import pipelines as pipes

class DummyComponent1:
    def __init__(self, df, options={}):
        self.df = df 
        self.options = options 
        self.cols_to_drop = ['test_col_1']

    def run(self):
        return self.df.drop(self.cols_to_drop, axis=1)

class DummyComponent2:
    def __init__(self, df, options={}):
        self.df = df 
        self.options = options 
        self.cols_to_drop = ['test_col_2']

    def run(self):
        return self.df.drop(self.cols_to_drop, axis=1)

def test_pipeline_with_no_components():
    input_df = pd.DataFrame(
        {
            'test_col_1': [1, 2, 3],
            'test_col_2': [4, 5, 6]
        }
    )

    result_df = pipes.GenericPipeline(input_df, []).run()

    expected_df = pd.DataFrame(
        {
            'test_col_1': [1, 2, 3],
            'test_col_2': [4, 5, 6]
        }
    )

    pd.testing.assert_frame_equal(result_df, expected_df)

def test_pipeline_with_one_component():
    input_df = pd.DataFrame(
        {
            'test_col_1': [1, 2, 3],
            'test_col_2': [4, 5, 6]
        }
    )

    result_df = pipes.GenericPipeline(
        input_df,
        [
            (
                DummyComponent1,
                {}
            )
        ]
    ).run()

    expected_df = pd.DataFrame(
        {
            'test_col_2': [4, 5, 6]
        }
    )

    pd.testing.assert_frame_equal(result_df, expected_df)

def test_pipeline_with_two_components():
    input_df = pd.DataFrame(
        {
            'test_col_1': [1, 2, 3],
            'test_col_2': [4, 5, 6],
            'test_col_3': [7, 8, 9]
        }
    )

    result_df = pipes.GenericPipeline(
        input_df,
        [
            (
                DummyComponent1,
                {}
            ),
            (
                DummyComponent2,
                {}
            )
        ]
    ).run()

    expected_df = pd.DataFrame(
        {
            'test_col_3': [7, 8, 9]
        }
    )

    pd.testing.assert_frame_equal(result_df, expected_df)