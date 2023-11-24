import pytest
from datetime import datetime, timedelta

from epic_event_CRM.contract.model import Contract


def test_contract_creation():
    contract = Contract(cost=1000.0, balance=500.0, statut=2, client_id=1)
    assert contract.cost == 1000.0
    assert contract.balance == 500.0
    assert contract.statut == 2
    assert contract.client_id == 1


def test_contract_id_property():
    contract = Contract(cost=1500.0, balance=800.0, client_id=2)
    assert contract.id == contract.contract_id


def test_contract_id_name_property():
    contract = Contract(cost=2000.0, balance=1000.0, client_id=3)
    assert contract.id_name == "contract_id"


def test_contract_creation_date():
    contract = Contract(cost=2500.0, balance=1200.0, client_id=4)
    today_date = datetime.now().strftime("%Y-%m-%d")
    assert contract.creation_date == today_date


def test_contract_last_update():
    contract = Contract(cost=3000.0, balance=1500.0, client_id=5)
    now_date = datetime.now()
    last_update_date = datetime.strptime(contract.last_update, "%Y-%m-%d %H:%M:%S")
    time_difference = now_date - last_update_date
    # Acceptons une différence de temps d'une seconde pour éviter des échecs intermittents
    assert time_difference < timedelta(seconds=2)
