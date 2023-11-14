from typing import Dict

from epic_event_CRM.base.context import Context
from epic_event_CRM.base.controller import BaseController
from epic_event_CRM.base.model import BaseModel
from epic_event_CRM.event.form import EventCreationForm
from epic_event_CRM.event.model import Event
from epic_event_CRM.event.serializer import EventSerializer
from epic_event_CRM.event.view import (
    EventView,
    UnassignedEventView,
    UserAssignedEventView,
    EventCreateView,
    CommercialClientEventView,
)


class EventController(BaseController):
    views = [
        EventView,
        UnassignedEventView,
        UserAssignedEventView,
        EventCreateView,
        CommercialClientEventView,
    ]
    serializers = EventSerializer

    model = Event
    form = EventCreationForm
    table = "event"

    @classmethod
    def create(cls, context: Context, form: Dict = None) -> BaseModel:
        if form is None:
            form = cls.fill_obj_form(context)
        if context.get_in_context("contract"):
            contract = context.get_in_context("contract")
            form["contract_id"] = contract.id
        return super().create(context, form)
