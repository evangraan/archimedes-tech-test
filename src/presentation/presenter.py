import pandas as pd
from pandas import DataFrame
import json
import csv
from csv import writer
from datetime import datetime
import dateutil


class IPresenter:
    def present(self, data_frame: DataFrame, path: str):
        raise NotImplementedError


class Presenter:
    def get(presentation_format: str) -> IPresenter:
        if presentation_format == "csv":
            return CSVPresenter()
        return None


class CSVPresenter(IPresenter):
    def present(self, data_frame: DataFrame, path: str):
        with open(path, 'w', newline='') as csvfile:
            writer = csv.writer(csvfile)
            self._present_header(writer)
            self._present_entries(data_frame, writer)

    def _present_header(self, writer: writer):
        writer.writerow(['id', 'date', 'number', 'operator', 'riskScore'])

    def _present_entries(self, data_frame: DataFrame, writer: writer):
        for index, entry in data_frame.iterrows():
            self._present_entry(entry, writer)

    def _present_entry(self, entry: dict, writer: writer):
        if str(entry['attributes']) == 'nan':
            entry['attributes'] = {'operator': 'Unknown'}
        self._present_entry_fields(entry, writer)

    def _present_entry_fields(self, entry: dict, writer: writer):
        writer.writerow([entry['id_x'],
                         entry['date'],
                         entry['number'],
                         entry['attributes']['operator'],
                         entry['riskScore']])

