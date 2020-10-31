import pytest

from ingestion import ingestor
from preparation import preparator
from enrichment import enricher


@pytest.fixture
def enrich():
    ing = ingestor.Ingestor.get("json")
    calls = preparator.Preparator.get("calls").prepare(
        ing.ingest("tests/data/calls.json"))
    operators = preparator.Preparator.get("operators").prepare(
        ing.ingest("tests/data/operators.json"))
    enr = enricher.Enricher()
    return {'output': enr.enrich(calls, operators)}


def test_merge(enrich):
    print("Enrichment: it should merge all calls")
    output = enrich['output']
    assert len(output) == 50


def test_merge_operator(enrich):
    print("Enrichment: it should merge in the operator name")
    output = enrich['output']
    assert output.iloc[19]['number'] == "Withheld"
    assert output.iloc[17]['attributes']['operator'] == "O2"


def test_sort(enrich):
    print("Enrichment: It should sort the calls by date, ascending")
    output = enrich['output']
    assert output.iloc[0]['date'] == '2018-02-20'
    assert output.iloc[49]['date'] == '2020-09-17'

