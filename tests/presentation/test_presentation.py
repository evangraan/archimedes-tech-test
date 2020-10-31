import pytest
import os.path
import pandas as pd
from ingestion import ingestor
from preparation import preparator
from enrichment import enricher
from presentation import presenter


@pytest.fixture
def export():
    ing = ingestor.Ingestor.get("json")
    calls = preparator.Preparator.get("calls").prepare(
        ing.ingest("tests/data/calls.json"))
    operators = preparator.Preparator.get("operators").prepare(
        ing.ingest("tests/data/operators.json"))
    enr = enricher.Enricher()
    presenter.Presenter.get("csv").present(
        enr.enrich(calls, operators), "output.csv")


def test_export(export):
    print("Enrichment: it should export a dictionary to a specified JSON file")
    assert os.path.exists("output.csv")
    df_output = pd.read_csv("output.csv")
    assert len(df_output) == 50


def test_correctness(export):
    print("""Enrichment: it should accurately export
             id, date, number, operator, riskScore""")
    df_output = pd.read_csv("output.csv")
    assert df_output.iloc[49]['id'] == "c7e0e4da-8a2b-4f71-89ac-fd9554e14e19"
    assert df_output.iloc[49]['date'] == "2020-09-17"
    assert df_output.iloc[49]['number'] == "+44381"
    assert df_output.iloc[49]['operator'] == "EE"
    assert df_output.iloc[49]['riskScore'] == 1.0


def test_sorted(export):
    print("Enrichment: it should export sorted by date ascending")
    df_output = pd.read_csv("output.csv")
    assert df_output.iloc[0]['date'] == "2018-02-20"
    assert df_output.iloc[49]['date'] == "2020-09-17"

