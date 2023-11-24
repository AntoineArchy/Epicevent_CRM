from typing import Dict

from base.context import Context
from base.controller import BaseController
from base.model import BaseModel
from epic_event_CRM.collaborator.controller import CollaboratorController
from epic_event_CRM.collaborator.view import SupportCollaboratorView
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

    @classmethod
    def get_answer(cls, context, question):
        if question in cls.form.questions:
            return context.display.fill_form(form_data=question)

        elif question == "Select_Collaborator":
            selected_collaborator = CollaboratorController.handle_user_select(
                context, SupportCollaboratorView
            )
            if selected_collaborator is not None:
                return {"support_contact": selected_collaborator.id}
