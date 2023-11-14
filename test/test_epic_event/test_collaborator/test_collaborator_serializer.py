from epic_event_CRM.base import authorization
from epic_event_CRM.collaborator.model import Collaborator
from epic_event_CRM.collaborator.serializer import CollaboratorSerializer


def test_create_authorization():
    serializer = CollaboratorSerializer()
    assert isinstance(serializer.create_authorization[0](), authorization.IsGestion)


def test_from_obj_dict_to_view_data():
    collaborator = Collaborator(
        department="sales",
        first_name="John",
        last_name="Doe",
        username="jdoe",
        password="secret",
        creation_date="2023-11-10",
        collaborator_id=1,
    )

    expected_result = {
        "Département": "sales",
        "Prénom": "John",
        "Nom d'utilisateur (EpicEvent/Mysql)": "Doe",
        "Mot de passe (provisoire)": "jdoe",
        "Collaborateur depuis": "2023-11-10",
        "Collaborateur ID": 1,
    }

    result = CollaboratorSerializer.from_obj_dict_to_view_data(collaborator.__dict__)
    assert result == expected_result


def test_get_obj_dict():
    collaborator = Collaborator(
        department="marketing",
        first_name="Jane",
        last_name="Smith",
        username="jsmith",
        password="pass123",
        creation_date="2023-11-10",
        collaborator_id=2,
    )

    expected_result = {
        "department": "marketing",
        "first_name": "Jane",
        "last_name": "Smith",
        "username": "jsmith",
        "password": "pass123",
        "creation_date": "2023-11-10",
        "collaborator_id": 2,
    }

    result = CollaboratorSerializer.get_obj_dict(collaborator)

    assert result == expected_result


def test_from_view_data_to_obj_dict():
    view_data = {
        "Département": "development",
        "Prénom": "Alice",
        "Nom": "Johnson",
        "téléphone": "ajohnson",
        "Collaborateur depuis": "2023-11-10",
    }

    expected_result = {
        "department": "development",
        "first_name": "Alice",
        "last_name": "Johnson",
        "username": "ajohnson",
        "creation_date": "2023-11-10",
    }

    result = CollaboratorSerializer.from_view_data_to_obj_dict(view_data)

    print(result)
    print(expected_result)
    assert result == expected_result
