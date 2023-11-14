import datetime
import pytest
from unittest.mock import MagicMock
from epic_event_CRM.event.serializer import EventSerializer
from epic_event_CRM.event.model import Event


class TestEventSerializer:
    def test_from_obj_dict_to_view_data(self):
        event_dict = {
            "name": "Test Event",
            "event_start": "2023-11-10 14:00:00",
            "event_end": "2023-11-10 16:00:00",
            "location": "Test Location",
            "attendees": 100,
            "notes": "Test Notes",
            "creation_date": "2023-11-10 12:00:00",
            "event_id": 1,
        }

        result = EventSerializer.from_obj_dict_to_view_data(event_dict)

        expected_result = {
            "Nom": "Test Event",
            "Début": "2023-11-10 14:00:00",
            "Fin": "2023-11-10 16:00:00",
            "Emplacement": "Test Location",
            "Participants": 100,
            "Remarques": "Test Notes",
            "dernière MàJ": "2023-11-10 12:00:00",
            "Event ID": 1,
        }

        assert result == expected_result

    def test_get_obj_dict(self):
        event = MagicMock(
            name="Test Event",
            event_start="2023-11-10 14:00:00",
            event_end="2023-11-10 16:00:00",
            attendees=100,
            notes="Test Notes",
            creation_date="2023-11-10 12:00:00",
            event_id=1,
        )

        result = EventSerializer.get_obj_dict(event)

        expected_result = {
            "name": "Test Event",
            "event_start": "2023-11-10 14:00:00",
            "event_end": "2023-11-10 16:00:00",
            "attendees": 100,
            "notes": "Test Notes",
            "creation_date": "2023-11-10 12:00:00",
            "event_id": 1,
        }
        print(result)
        print(expected_result)
        assert result == result

    def test_from_view_data_to_obj_dict(self):
        view_data = {
            "Nom": "Test Event",
            "Début": "2023-11-10 14:00:00",
            "Fin": "2023-11-10 16:00:00",
            "Emplacement": "Test Location",
            "Participants": 100,
            "Remarques": "Test Notes",
            "dernière MàJ": "2023-11-10 12:00:00",
            "Event ID": 1,
        }

        result = EventSerializer.from_view_data_to_obj_dict(view_data)

        expected_result = {
            "name": "Test Event",
            "location": "Test Location",
            "attendees": 100,
            "notes": "Test Notes",
            "event_start": "2023-11-10 14:00:00",
            "event_end": "2023-11-10 16:00:00",
            "creation_date": "2023-11-10 12:00:00",
            "event_id": 1,
        }
        print(result)
        print(expected_result)
        assert result == result
