from epic_event_CRM.base import authorization
from epic_event_CRM.base.view import BaseView, CreateView


class ContractView(BaseView):
    view_name = "list_contract"
    name_display = "Voir tous les contrats"

    allow_select = True


class UserClientContractView(ContractView):
    view_name = "commercial_client_contracts"
    name_display = "Voir les contrats de mes clients"

    view_authorization = [authorization.IsCommercial]


class CreateContractView(CreateView):
    name_display = "Créer un contrat"

    view_authorization = [authorization.IsNotSupport]
    context_requirements = ["client"]
