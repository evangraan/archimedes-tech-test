import pandas as pd
from datetime import datetime
import dateutil

epoch = dateutil.parser.parse("1970-01-01T00:00:00.00Z")


class IPreparator:
    def prepare(self, operators_data: list):
        raise NotImplementedError


class Preparator:
    def get(preparation: str) -> IPreparator:
        if preparation == "calls":
            return CallsPreparator()
        if preparation == "operators":
            return OperatorsPreparator()
        raise NotImplementedError


class OperatorsPreparator(IPreparator):
    def prepare(self, operators_data: list) -> dict:
        operators = []
        for entry in operators_data:
            entry['prefix'] = entry['attributes']['prefix']
            operators.append(entry)
        return {'operators': operators}


class CallsPreparator(IPreparator):
    def prepare(self, calls_data: list) -> dict:
        calls = []
        for entry in calls_data:
            calls.append(self._prepare_entry(entry))
        return {'calls': calls}

    def _prepare_entry(self, entry: dict) -> dict:
        entry = self._prepare_entry_date_and_timestamp(entry)
        entry = self._map_attributes(entry)
        return entry

    def _prepare_entry_date_and_timestamp(self, entry: dict) -> dict:
        if self._has_attr(entry, 'date'):
            entry = self._transform_entry_datetime(entry)
        else:
            entry = self._unknown_entry_datetime(entry)
        return entry

    def _map_attributes(self, entry: dict) -> dict:
        if not self._has_attr(entry, 'number'):
            entry = self._map_no_number_attributes(entry)
        else:
            entry = self._map_number_attributes(entry)
        del entry['attributes']
        return entry

    def _transform_entry_datetime(self, entry: dict) -> dict:
        dt = dateutil.parser.parse(entry['attributes']['date'])
        entry['date'] = dt.strftime('%Y-%m-%d')
        entry['timestamp'] = (dt - epoch).total_seconds()
        return entry

    def _unknown_entry_datetime(self, entry: dict) -> dict:
        entry['date'] = 'Unknown'
        entry['timestamp'] = epoch
        return entry

    def _map_no_number_attributes(self, entry: dict) -> dict:
        entry['number'] = 'Withheld'
        entry['prefix'] = None
        return entry

    def _map_number_attributes(self, entry: dict) -> dict:
        entry['number'] = entry['attributes']['number'][0:6]
        entry = self._prepare_entry_risk_score(entry)
        entry['prefix'] = str(entry['attributes']['number'][3:4]) + "000"
        return entry

    def _prepare_entry_risk_score(self, entry: dict) -> dict:
        if self._has_attr(entry, 'riskScore'):
            entry = self._determine_risk_score_precedence(entry)
        return entry

    def _determine_risk_score_precedence(self, entry: dict) -> dict:
        entry = self._simplify_risk_score(entry)
        entry = self._enforce_red_list(entry)
        entry = self._enforce_green_list(entry)
        return entry

    def _simplify_risk_score(self, entry: dict) -> dict:
        entry['riskScore'] = str(round(
            float(entry['attributes']['riskScore']), 1))
        return entry

    def _enforce_red_list(self, entry: dict) -> dict:
        if self._is_red_listed(entry):
            entry['riskScore'] = 1.0
        return entry

    def _enforce_green_list(self, entry: dict) -> dict:
        if self._is_green_listed(entry):
            entry['riskScore'] = 0.0
        return entry

    def _has_attr(self, entry: dict, attribute: str) -> bool:
        return attribute in entry['attributes']

    def _is_red_listed(self, entry: dict) -> bool:
        return 'redList' in entry['attributes'] and \
               entry['attributes']['redList'] is True

    def _is_green_listed(self, entry: dict) -> bool:
        return 'greenList' in entry['attributes'] and \
               entry['attributes']['greenList'] is True

