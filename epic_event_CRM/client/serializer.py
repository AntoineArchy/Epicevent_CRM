import datetime

from epic_event_CRM.base import authorization
from epic_event_CRM.base.serializer import BaseSerializer
from epic_event_CRM.client.model import Client


class ClientSerializer(BaseSerializer):
    model = Client
    table = "client"

    create_authorization = [authorization.IsCommercial]

    name_display = "Créer un nouveau client"

    @classmethod
    def from_obj_dict_to_view_data(cls, obj_dict):
        return {
            "Client ID": obj_dict.get("client_id"),
            "Société": obj_dict.get("company_name"),
            "Intérlocuteur": obj_dict.get("full_name"),
            "adresse mail": obj_dict.get("email"),
            "téléphone": obj_dict.get("phone"),
            "client depuis": obj_dict.get("creation_date"),
            "dernier contact": obj_dict.get("last_update"),
            "Commercial associé": obj_dict.get("collaborator_id"),
        }

    @classmethod
    def get_blank_form(cls):
        return {
            "full_name": str,
            "company_name": str,
            "email": str,
            "phone": str,
            "creation_date": datetime.datetime.now().strftime("%Y-%m-%d"),
            "last_update": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "client_id": -1,
        }

    @classmethod
    def get_obj_dict(cls, obj: Client):
        return {
            "full_name": obj.full_name,
            "company_name": obj.company_name,
            "email": obj.email,
            "phone": obj.phone,
            "creation_date": obj.creation_date,
            "last_update": obj.last_update,
            "client_id": obj.client_id,
            "collaborator_id": obj.collaborator_id,
        }

    @classmethod
    def from_view_data_to_obj_dict(cls, view_data):
        from_view_dict = {
            "full_name": view_data.get("Intérlocuteur", "Non transmis"),
            "company_name": view_data.get("Société", "Non transmis"),
            "email": view_data.get("adresse mail", "Non transmis"),
            "phone": view_data.get("téléphone", "Non transmis"),
            "creation_date": view_data.get(
                "client depuis", datetime.datetime.now().strftime("%Y-%m-%d")
            ),
            "last_update": view_data.get(
                "dernier contact", datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            ),
            "client_id": view_data.get("Client ID", -1),
        }

        return from_view_dict
