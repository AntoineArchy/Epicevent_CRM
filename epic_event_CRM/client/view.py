from base import authorization
from base.view import BaseView, CreateView


class ClientView(BaseView):
    view_name = "list_client"
    name_display = "Voir tous les clients"

    select_authorization = [authorization.IsGestion]


class UserOwnClientView(ClientView):
    view_name = "commercial_own_client"
    name_display = "Voir mes clients"

    view_authorization = [authorization.IsCommercial]
    select_authorization = [authorization.IsCommercial]
    update_authorization = [authorization.IsCommercial]
    delete_authorization = [authorization.Forbidden]


class CreateClientView(CreateView):
    name_display = "Créer un nouveau client"

    view_authorization = [authorization.IsCommercial]
