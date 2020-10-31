import pytest

from ingestion import ingestor
from preparation import preparator


@pytest.fixture
def preparation():
    ing = ingestor.Ingestor.get("json")
    calls_data = ing.ingest("tests/data/calls.json")
    prep = preparator.Preparator.get("calls")
    return prep.prepare(calls_data)


def test_preparation(preparation):
    print("""Preparation: it should include
          id, number, prefix, riskScore, datetime, timestamp and attributes""")

    calls = preparation['calls']
    call = calls[10]
    assert 'id' in call
    assert 'number' in call
    assert 'prefix' in call
    assert 'riskScore' in call
    assert 'date' in call
    assert 'timestamp' in call
    assert 'attributes' not in call


def test_date_format(preparation):
    print("Preparation: it should format the date as YYYY-MM-DD")
    calls = preparation['calls']
    call = calls[0]
    assert call['date'] == '2020-03-06'


def test_timestamp(preparation):
    print("Preparation: it should calculate a timestamp for sorting")
    calls = preparation['calls']
    call = calls[0]
    assert str(call['timestamp']) == '1583530696.0'


def test_number_withheld(preparation):
    print("Preparation: it should set number to Withheld if not present")
    calls = preparation['calls']
    call = calls[0]
    assert call['number'] == 'Withheld'


def test_number(preparation):
    print("""Preparation: it should use the first 6 characters
          of the number only""")
    calls = preparation['calls']
    call = calls[1]
    assert call['number'] == '+44364'


def test_no_prefix_if_no_number(preparation):
    print("Preparation: it should set prefix to None if number not present")
    calls = preparation['calls']
    call = calls[0]
    assert call['prefix'] is None


def test_prefix(preparation):
    print("""Preparation: it should round the first 4 digits of
          the number excluding country code down to the lower thousand""")
    calls = preparation['calls']
    call = calls[1]
    assert call['prefix'] == '3000'


def test_riskScore(preparation):
    print("Preparation: it should round riskScore to 1 decimal point")
    calls = preparation['calls']
    call = calls[21]
    assert call['riskScore'] == 1.0


def test_greenList(preparation):
    print("Preparation: it should set riskScore to 0.0 if greenList is True")
    calls = preparation['calls']
    call = calls[3]
    assert call['riskScore'] == 0.0


def test_greenList(preparation):
    print("Preparation: it should set riskScore to 1.0 if redList is True")
    calls = preparation['calls']
    call = calls[20]
    assert call['riskScore'] == 1.0


def test_greenList_precedence(preparation):
    print("""Preparation: it should set riskScore to 0.0 if both
          redList and greenList is True""")
    calls = preparation['calls']
    call = calls[1]
    assert call['riskScore'] == 0.0


def test_operator_prefix():
    print("Preparation: it should include prefix at the top level")
    ing = ingestor.Ingestor.get("json")
    operators = ing.ingest("tests/data/operators.json")
    prep = preparator.Preparator.get("operators")
    operators = prep.prepare(operators)["operators"]
    assert operators[0]['prefix'] == '3000'

