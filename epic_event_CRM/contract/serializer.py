import datetime

from epic_event_CRM.base import authorization
from epic_event_CRM.base.serializer import BaseSerializer

from epic_event_CRM.contract.form import ContractCreationForm
from epic_event_CRM.contract.model import Contract


class ContractSerializer(BaseSerializer):
    model = Contract
    form = ContractCreationForm
    table = "contract"

    create_authorization = [authorization.IsCommercial, authorization.IsGestion]

    name_display = "Créer un nouveau contrat"

    @classmethod
    def from_obj_dict_to_view_data(cls, obj_dict):
        return {
            "Montant total": obj_dict.get("cost"),
            "Reste à payer": obj_dict.get("balance"),
            "Statut": obj_dict.get("statut"),
            # "adresse mail": obj_dict.get("email"),
            # "téléphone": obj_dict.get("phone"),
            "Sous contrat depuis": obj_dict.get("creation_date"),
            "dernière MàJ": obj_dict.get("last_update"),
            "Client ID": obj_dict.get("client_id"),
            "Contrat ID": obj_dict.get("contract_id"),
        }

    @classmethod
    def get_obj_dict(cls, obj: Contract):
        return {
            "cost": obj.cost,
            "balance": obj.balance,
            "statut": obj.statut,
            # "phone": obj.phone,
            "creation_date": obj.creation_date,
            "last_update": obj.last_update,
            "client_id": obj.client_id,
            "contract_id": obj.contract_id,
        }

    @classmethod
    def from_view_data_to_obj_dict(cls, view_data):
        from_view_dict = {
            "cost": view_data.get("Montant total", "Non transmis"),
            "balance": view_data.get("Reste à payer", "Non transmis"),
            "statut": view_data.get("Statut", "Non transmis"),
            "creation_date": view_data.get(
                "Sous contrat depuis", datetime.datetime.now().strftime("%Y-%m-%d")
            ),
            "last_update": view_data.get(
                "Dernière MàJ", datetime.datetime.now().strftime("%Y-%m-%d")
            ),
            "contract_id": view_data.get("Contrat ID", -1),
            "client_id": view_data.get("Client ID", -1),
        }
        print(view_data)
        print(from_view_dict)
        return from_view_dict
