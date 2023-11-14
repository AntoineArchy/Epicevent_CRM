from datetime import datetime

from epic_event_CRM.base.authorization import IsCommercial
from epic_event_CRM.client.model import Client
from epic_event_CRM.client.serializer import ClientSerializer


def test_create_authorization():
    serializer = ClientSerializer()
    print(serializer.create_authorization)
    assert isinstance(serializer.create_authorization[0](), IsCommercial)


def test_name_display():
    serializer = ClientSerializer()
    assert serializer.name_display == "Créer un nouveau client"


def test_from_obj_dict_to_view_data():
    obj_dict = {
        "client_id": 1,
        "company_name": "ABC Corp",
        "full_name": "John Doe",
        "email": "john.doe@example.com",
        "phone": "123456789",
        "creation_date": "2023-11-10",
        "last_update": "2023-11-10 13:29:48",
        "collaborator_id": 2,
    }

    expected_view_data = {
        "Client ID": 1,
        "Société": "ABC Corp",
        "Intérlocuteur": "John Doe",
        "adresse mail": "john.doe@example.com",
        "téléphone": "123456789",
        "client depuis": "2023-11-10",
        "dernier contact": "2023-11-10 13:29:48",
        "Commercial associé": 2,
    }

    assert ClientSerializer.from_obj_dict_to_view_data(obj_dict) == expected_view_data


def test_get_blank_form():
    blank_form = ClientSerializer.get_blank_form()
    assert blank_form == {
        "full_name": str,
        "company_name": str,
        "email": str,
        "phone": str,
        "creation_date": datetime.now().strftime("%Y-%m-%d"),
        "last_update": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "client_id": -1,
    }


def test_get_obj_dict():
    client = Client(
        client_id=1,
        company_name="ABC Corp",
        full_name="John Doe",
        email="john.doe@example.com",
        phone="123456789",
        creation_date="2023-11-10",
        last_update="2023-11-10 13:29:48",
        collaborator_id=2,
    )

    expected_obj_dict = {
        "full_name": "John Doe",
        "company_name": "ABC Corp",
        "email": "john.doe@example.com",
        "phone": "123456789",
        "creation_date": "2023-11-10",
        "last_update": "2023-11-10 13:29:48",
        "client_id": 1,
        "collaborator_id": 2,
    }

    assert ClientSerializer.get_obj_dict(client) == expected_obj_dict


def test_from_view_data_to_obj_dict():
    view_data = {
        "Client ID": 1,
        "Société": "ABC Corp",
        "Intérlocuteur": "John Doe",
        "adresse mail": "john.doe@example.com",
        "téléphone": "123456789",
        "client depuis": "2023-11-10",
        "dernier contact": "2023-11-10 13:29:48",
        "Commercial associé": 2,
    }

    expected_obj_dict = {
        "full_name": "John Doe",
        "company_name": "ABC Corp",
        "email": "john.doe@example.com",
        "phone": "123456789",
        "creation_date": "2023-11-10",
        "last_update": "2023-11-10 13:29:48",
        "client_id": 1,
    }

    assert ClientSerializer.from_view_data_to_obj_dict(view_data) == expected_obj_dict
