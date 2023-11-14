from epic_event_CRM.base import authorization
from epic_event_CRM.base.view import BaseView, CreateView


class CollaboratorView(BaseView):
    view_name = "list_collaborator"
    name_display = "Voir mes collaborateurs"

    allow_select = True


class CreateCollaboratorView(CreateView):
    name_display = "Créer un collaborateur"

    view_authorization = [authorization.IsGestion]
