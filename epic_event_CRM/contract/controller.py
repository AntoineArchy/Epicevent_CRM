from typing import Dict

from base.context import Context
from base.controller import BaseController
from base.model import BaseModel
from epic_event_CRM.contract.form import ContractCreationForm
from epic_event_CRM.contract.model import Contract
from epic_event_CRM.contract.serializer import ContractSerializer
from epic_event_CRM.contract.view import (
    ContractView,
    UserClientContractView,
    CreateContractView,
    UnPayedContract,
    UnsignedContract,
)


class ContractController(BaseController):
    views = [
        ContractView,
        UserClientContractView,
        CreateContractView,
        UnsignedContract,
        UnPayedContract,
    ]
    serializers = ContractSerializer

    table = "contract"
    model = Contract
    form = ContractCreationForm

    @classmethod
    def create(cls, context: Context, form: Dict = None) -> BaseModel:
        if form is None:
            form = cls.fill_obj_form(context)

        if not form.get("client_id", False):
            client = context.get_in_context("client")
            form["client_id"] = client.id
        return super().create(context, form)
