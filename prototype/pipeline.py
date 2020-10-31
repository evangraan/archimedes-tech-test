import pandas as pd
import sqlite3
import json
import csv
from datetime import datetime
import dateutil

epoch = dateutil.parser.parse("1970-01-01T00:00:00.00Z")
calls = []
calls_data = None
with open("/Users/ernst/scratch/archimedes-tech-test/data/calls.json") as json_file:
    calls_data = json.load(json_file)["data"]

for entry in calls_data:
    dt = dateutil.parser.parse(entry['attributes']['date'])
    entry['date'] = dt.strftime('%Y-%m-%d')
    entry['timestamp'] = (dt - epoch).total_seconds()
    if not 'number' in entry['attributes']:
        entry['number'] = 'Withheld'
        entry['prefix'] = None
    else:
        entry['number'] = entry['attributes']['number'][0:6]
        if 'riskScore' in entry['attributes']:
            entry['riskScore'] = str(round(float(entry['attributes']['riskScore']), 1))
            if 'redList' in entry['attributes'] and entry['attributes']['redList'] == True:
                entry['riskScore'] = 1.0
            if 'greenList' in entry['attributes'] and entry['attributes']['greenList'] == True:
                entry['riskScore'] = 0.0

        entry['prefix'] = str(entry['attributes']['number'][3:4]) + "000"
    del entry['attributes']
    calls.append(entry)

operators = []
operators_data = None
with open("/Users/ernst/scratch/archimedes-tech-test/data/operators.json") as json_file:
    operators_data = json.load(json_file)["data"]

for entry in operators_data:
    entry['prefix'] = entry['attributes']['prefix']
    operators.append(entry)

df_calls = pd.DataFrame.from_dict(calls)
df_operators = pd.DataFrame.from_dict(operators)
df_merged = pd.merge(df_calls, df_operators, how='outer', on='prefix')
df_merged.sort_values(by=['timestamp'], inplace=True)

with open('output.csv', 'w', newline='') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(['id','date','number','operator','riskScore'])
    for index, entry in df_merged.iterrows():
        if str(entry['attributes']) == 'nan':
            entry['attributes'] = {'operator' : 'Unknown'}
        writer.writerow([entry['id_x'], entry['date'], entry['number'], entry['attributes']['operator'], entry['riskScore']])
