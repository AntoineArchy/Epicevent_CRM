from base import authorization
from base.view import BaseView, CreateView
from epic_event_CRM.contract.form import ContractStatus


class EventView(BaseView):
    view_name = "list_event"
    name_display = "Voir tous les événements"


class EventCreateView(CreateView):
    name_display = "Créer un évènement"

    context_requirements = ["contract"]

    @classmethod
    def are_requirements_meet(cls, context) -> bool:
        if not super().are_requirements_meet(context):
            return False

        contract = context.get_in_context("contract")
        return contract.statut.lower() != ContractStatus.to_sign.value.lower()


class UnassignedEventView(EventView):
    allow_select = True

    view_name = "unassigned_event"
    name_display = "Voir les événements non assigné"

    view_authorization = [authorization.IsGestion]


class UserAssignedEventView(UnassignedEventView):
    view_name = "user_assigned_event"
    name_display = "Voir les événements qui me sont assignés"

    view_authorization = [authorization.IsSupport]
    select_authorization = [authorization.IsSupport]
    update_authorization = [authorization.IsSupport]


class CommercialClientEventView(UnassignedEventView):
    view_name = "commercial_client_event_view"
    name_display = "Voir les événements de mes clients"

    view_authorization = [authorization.IsCommercial]
