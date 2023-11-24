import datetime

from base import authorization
from base.serializer import BaseSerializer

from epic_event_CRM.event.form import EventCreationForm
from epic_event_CRM.event.model import Event


class EventSerializer(BaseSerializer):
    model = Event
    form = EventCreationForm
    table = "event"

    create_authorization = [authorization.IsCommercial]

    name_display = "Créer un nouvel événement"

    @classmethod
    def from_obj_dict_to_view_data(cls, obj_dict):
        return {
            "Nom": obj_dict.get("name"),
            "Début": obj_dict.get("event_start"),
            "Fin": obj_dict.get("event_end"),
            "Emplacement": obj_dict.get("location"),
            "Participants": obj_dict.get("attendees"),
            "Remarques": obj_dict.get("notes"),
            "dernière MàJ": obj_dict.get("creation_date"),
            "Event ID": obj_dict.get("event_id"),
            # "Contrat ID": obj_dict.get("contract_id"),
        }

    @classmethod
    def get_obj_dict(cls, obj: Event):
        return {
            "name": obj.name,
            "event_start": obj.event_start,
            "event_end": obj.event_end,
            "location": obj.location,
            "attendees": obj.attendees,
            "notes": obj.notes,
            "creation_date": obj.creation_date,
            "event_id": obj.event_id,
        }

    @classmethod
    def from_view_data_to_obj_dict(cls, view_data):
        from_view_dict = {
            "name": view_data.get("Événement", "Non transmis"),
            "location": view_data.get("Lieu", "Non transmis"),
            "attendees": view_data.get("Participants", "Non transmis"),
            "notes": view_data.get("Notes", "Non transmis"),
            "event_start": view_data.get(
                "Début", datetime.datetime.now().strftime("%Y-%m-%d")
            ),
            "event_end": view_data.get(
                "Fin", datetime.datetime.now().strftime("%Y-%m-%d")
            ),
            "creation_date": view_data.get(
                "Sous contrat depuis", datetime.datetime.now().strftime("%Y-%m-%d")
            ),
            # "last_update": view_data.get(
            #     "Dernière MàJ", datetime.datetime.now().strftime("%Y-%m-%d")
            # ),
            # "contract_id": view_data.get("Contrat N°", -1),
            "event_id": view_data.get("Event ID", -1),
        }

        return from_view_dict
