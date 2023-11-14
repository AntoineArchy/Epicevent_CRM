from epic_event_CRM.base import authorization
from epic_event_CRM.base.view import BaseView, CreateView


class ClientView(BaseView):
    view_name = "list_client"
    name_display = "Voir tous les clients"

    allow_select = True


class UserOwnClientView(ClientView):
    view_name = "commercial_own_client"
    name_display = "Voir mes clients"

    view_authorization = [authorization.IsCommercial]


class CreateClientView(CreateView):
    name_display = "Créer un nouveau client"

    view_authorization = [authorization.IsNotSupport]
