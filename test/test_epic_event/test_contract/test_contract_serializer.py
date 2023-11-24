from epic_event_CRM.contract.model import Contract
from epic_event_CRM.contract.serializer import ContractSerializer


def test_from_obj_dict_to_view_data():
    # Créer un objet Contract fictif
    contract = Contract(cost=3000.0, balance=1500.0, statut=2, client_id=5)

    # Utiliser le serializer pour convertir l'objet en un dictionnaire de données de vue
    view_data = ContractSerializer.from_obj_dict_to_view_data(contract.__dict__)

    # Vérifier que les champs attendus sont présents dans le dictionnaire
    assert "Montant total" in view_data
    assert "Reste à payer" in view_data
    assert "Statut" in view_data
    assert "Sous contrat depuis" in view_data
    assert "dernière MàJ" in view_data
    assert "Client ID" in view_data
    assert "Contrat ID" in view_data


def test_get_obj_dict():
    # Créer un dictionnaire fictif de données de vue
    view_data = {
        "Cout": 3000.0,
        "Balance": 1500.0,
        "Statut": 2,
        "Sous contrat depuis": "2023-11-10",
        "Dernière MàJ": "2023-11-10 14:19:47",
        "Client ID": 5,
        "Contrat ID": 10,
    }

    # Utiliser le serializer pour convertir le dictionnaire en un dictionnaire d'objet Contract
    obj_dict = ContractSerializer.from_view_data_to_obj_dict(view_data)
    print(obj_dict)
    # Vérifier que les champs attendus sont présents dans le dictionnaire
    assert "cost" in obj_dict
    assert "balance" in obj_dict
    assert "statut" in obj_dict
    assert "creation_date" in obj_dict
    assert "last_update" in obj_dict
    assert "client_id" in obj_dict
    assert "contract_id" in obj_dict

    # Vérifier que les valeurs sont correctes
    assert obj_dict["cost"] == view_data["Cout"]
    assert obj_dict["balance"] == view_data["Balance"]
    assert obj_dict["statut"] == view_data["Statut"]
    assert obj_dict["creation_date"] == view_data["Sous contrat depuis"]
    assert obj_dict["last_update"] == view_data["Dernière MàJ"]
    assert obj_dict["client_id"] == view_data["Client ID"]
    assert obj_dict["contract_id"] == view_data["Contrat ID"]
