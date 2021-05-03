import pandas as pd

class Component:
    def __init__(self, df, options={}):
        self.df = df 
        self.options = options 

    def _validate_input_columns(self, required_columns: list, df_columns: list):
        does_df_have_required_columns = set(required_columns).issubset(set(df_columns))
        if not does_df_have_required_columns:
            raise ValueError(
                'Some or all required columns {} are not found in input dataframe columns {}'.format(
                    str(required_columns), str(df_columns)
                )
            )

class DropColumns(Component):
    def __init__(self, df, options={}):
        super().__init__(df, options)
        self.cols_to_drop = self.options.get(
            "columns_to_drop",
            []
        )
        required_columns = self.cols_to_drop
        self._validate_input_columns(required_columns, self.df.columns.values.tolist())
    
    def run(self):
        return self.df.drop(self.cols_to_drop, axis=1)

class ConvertDateAndTimeToDatetime(Component):
    def __init__(self, df, options={}):
        super().__init__(df, options)
        required_columns = ['date', 'time']
        self._validate_input_columns(required_columns, self.df.columns.values.tolist())
        self.timezone = self.options.get(
            "timezone",
            'US/Eastern'
        )
        self.cols_to_drop = ['date_and_time']

    def run(self):
        self.df['date_and_time'] = self.df['date'] + ' ' + self.df['time']

        date_time_format = '%B %d %Y %I:%M %p'
        self.df['datetime'] = self.df.apply(
            lambda row: pd.to_datetime(
                row['date_and_time'],
                format = date_time_format
            ),
            axis=1
        )

        self.df.datetime = self.df.datetime.dt.tz_localize(self.timezone)

        return self.df.drop(self.cols_to_drop, axis=1)

