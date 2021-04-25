#imports 
import pandas as pd

class ConvertDateAndTimeToDatetime:
    def __init__(self, df, options={}):
        self.df = df
        self.options = options
        self.cols_to_drop = ['date_and_time']
        self.cols_to_drop.extend(
            self.options.get(
                "columns_to_drop", 
                []
            )
        )
        self.timezone = self.options.get(
            "timezone",
            'US/Eastern'
        )

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

