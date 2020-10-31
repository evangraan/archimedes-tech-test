import pandas as pd
from pandas import DataFrame
import json
import csv
from datetime import datetime
import dateutil


class Enricher:
    def enrich(self, calls: dict, operators: dict) -> DataFrame:
        df_calls = pd.DataFrame.from_dict(calls["calls"])
        df_operators = pd.DataFrame.from_dict(operators["operators"])
        df_merged = pd.merge(df_calls, df_operators, how='outer', on='prefix')
        df_merged.sort_values(by=['timestamp'], inplace=True)
        return df_merged
