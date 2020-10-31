import pytest

from ingestion import ingestor


@pytest.fixture
def ingestion():
    ing = ingestor.Ingestor.get("json")
    calls = ing.ingest("tests/data/calls.json")
    return {'ingestor': ing, 'calls': calls}


def test_factory_method_json(ingestion):
    print("Ingestion: it should produce a JSON capable ingestor")
    assert ingestion['ingestor'] is not None


def test_ingest_all_lines(ingestion):
    print("Ingestion: it should read all lines from the JSON file")
    assert len(ingestion['calls']) == 50


def test_empty_file():
    print("Ingestion: it should support an empty JSON file")
    ing = ingestor.Ingestor.get("json")
    calls = ing.ingest("tests/data/empty.json", None)
    assert calls == {}


def test_no_file():
    print("""Ingestion: it should raise an exception
           if the file does note exist""")
    with pytest.raises(FileNotFoundError):
        ing = ingestor.Ingestor.get("json")
        calls = ing.ingest("tests/data/doesnotexist.json")


def test_ingest_call_data(ingestion):
    print("Ingestion: it should read all call data from the JSON file")
    calls = ingestion['calls']
    assert type(calls[1]['attributes']) is dict
    assert calls[1]['attributes']['date'] == "2018-02-20T03:06:32Z"
    assert calls[0]['id'] == "2b3bc470-72dd-45e1-8099-227a73ee9623"
    assert calls[1]['attributes']['number'] == "+443642728615"
    assert calls[3]['attributes']['date'] == "2020-09-05T21:55:38Z"
    assert calls[1]['attributes']['riskScore'] == 0.5349286929075624
    assert calls[1]['attributes']['greenList'] is True
    assert calls[1]['attributes']['redList'] is True


def test_ingest_operator_data(ingestion):
    print("Ingestion: it should read all operator data from the JSON file")
    ing = ingestor.Ingestor.get("json")
    operators = ing.ingest("tests/data/operators.json")
    assert operators[0]['id'] == "12d9b951-c125-4da0-a70f-609b7ac558d8"
    assert operators[1]['type'] == "operator"
    assert type(operators[1]['attributes']) is dict
    assert operators[1]['attributes']['prefix'] == "4000"
    assert operators[1]['attributes']['operator'] == "O2"

