import argparse
from ingestion import ingestor
from preparation import preparator
from enrichment import enricher
from presentation import presenter

parser = argparse.ArgumentParser(
    description='Analyze call log based on operators and call numbers')
parser.add_argument(
    '--calls',
    help='The JSON file containing call log entries',
    required=True)
parser.add_argument(
    '--operators',
    help='The JSON file containing operator entries',
    required=True)
parser.add_argument(
    '--output',
    help='Path to the output CSV call analysis',
    required=True)
args = parser.parse_args()

ing = ingestor.Ingestor.get("json")
calls = preparator.Preparator.get("calls").prepare(
    ing.ingest(args.calls))
operators = preparator.Preparator.get("operators").prepare(
    ing.ingest(args.operators))
enr = enricher.Enricher()
presenter.Presenter.get("csv").present(
    enr.enrich(calls, operators), args.output)
