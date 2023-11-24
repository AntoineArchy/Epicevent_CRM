from base import authorization
from base.roles import EpicEventRole
from base.view import BaseView, CreateView


class CollaboratorView(BaseView):
    view_name = "list_collaborator"
    name_display = "Voir mes collaborateurs"

    view_authorization = [authorization.IsGestion]
    select_authorization = [authorization.IsGestion]
    delete_authorization = [authorization.IsGestion]


class CreateCollaboratorView(CreateView):
    name_display = "Créer un collaborateur"

    view_authorization = [authorization.IsGestion]


class SupportCollaboratorView(CollaboratorView):
    filter = f"`Département` = '{EpicEventRole.support.value}'"
