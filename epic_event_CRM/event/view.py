from epic_event_CRM.base import authorization
from epic_event_CRM.base.view import BaseView, CreateView


class EventView(BaseView):
    view_name = "list_event"
    name_display = "Voir tous les événements"

    allow_select = True


class EventCreateView(CreateView):
    name_display = "Créer un évènement"

    context_requirements = ["contract"]


class UnassignedEventView(BaseView):
    view_name = "unassigned_event"
    name_display = "Voir les événements non assigné"

    view_authorization = [authorization.IsGestion]


class UserAssignedEventView(BaseView):
    view_name = "user_assigned_event"
    name_display = "Voir les événements qui me sont assignés"

    view_authorization = [authorization.IsSupport]


class CommercialClientEventView(EventView):
    view_name = "commercial_client_event_view"
    name_display = "Voir les événements de mes clients"

    view_authorization = [authorization.IsCommercial]
