from base import authorization
from base.view import BaseView, CreateView
from epic_event_CRM.contract.form import ContractStatus


class ContractView(BaseView):
    view_name = "list_contract"
    name_display = "Voir tous les contrats"

    select_authorization = [authorization.IsGestion]


class UserClientContractView(ContractView):
    view_name = "commercial_client_contracts"
    name_display = "Voir les contrats de mes clients"

    view_authorization = [authorization.IsCommercial]
    select_authorization = [authorization.IsCommercial]


class UnsignedContract(UserClientContractView):
    name_display = "Voir les contrats qui ne sont pas encore signés."

    filter = f"`Statut` = '{ContractStatus.to_sign.value}'"
    context_requirements = [UserClientContractView]


class UnPayedContract(UserClientContractView):
    name_display = "Voir les contrats qui ne sont pas encore payés."

    filter = f"`Statut` = '{ContractStatus.to_pay.value}'"
    context_requirements = [UserClientContractView]


class CreateContractView(CreateView):
    name_display = "Créer un contrat"

    view_authorization = [authorization.IsNotSupport]
    context_requirements = ["client"]
