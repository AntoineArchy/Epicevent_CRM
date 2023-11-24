import datetime

from base import authorization
from base.serializer import BaseSerializer

from epic_event_CRM.collaborator.form import CollaboratorCreationForm
from epic_event_CRM.collaborator.model import Collaborator


class CollaboratorSerializer(BaseSerializer):
    model = Collaborator
    form = CollaboratorCreationForm
    table = "collaborator"

    create_authorization = [authorization.IsGestion]

    name_display = "Créer un nouveau collaborateur"

    @classmethod
    def from_obj_dict_to_view_data(cls, obj_dict):
        return {
            "Département": obj_dict.get("department"),
            "Nom": obj_dict.get("last_name"),
            "Prénom": obj_dict.get("first_name"),
            "Nom affiché": obj_dict.get("username"),
            "Collaborateur depuis": obj_dict.get("creation_date"),
            "Collaborateur ID": obj_dict.get("collaborator_id"),
        }

    @classmethod
    def get_obj_dict(cls, obj: Collaborator):
        return {
            "department": obj.department,
            "first_name": obj.first_name,
            "last_name": obj.last_name,
            "username": obj.username,
            "password": obj.password,
            "creation_date": obj.creation_date,
            "collaborator_id": obj.collaborator_id,
            # "event_id": obj.event_id,
        }

    @classmethod
    def from_view_data_to_obj_dict(cls, view_data):
        from_view_dict = {
            "department": view_data.get("Département", "Non transmis"),
            "first_name": view_data.get("Prénom", "Non transmis"),
            "last_name": view_data.get("Nom", "Non transmis"),
            "username": view_data.get("Nom affiché", "Non transmis"),
            "creation_date": view_data.get(
                "Collaborateur depuis", datetime.datetime.now().strftime("%Y-%m-%d")
            ),
            "collaborator_id": view_data.get("Collaborateur ID", -1),
        }

        return from_view_dict
