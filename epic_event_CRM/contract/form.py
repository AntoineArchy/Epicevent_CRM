from enum import Enum

from epic_event_CRM.base.form import BaseForm


class ContractStatu(Enum):
    to_sign = 1
    signed = 2
    to_pay = 3
    payed = 4


class ContractCreationForm(BaseForm):
    fields_display = ["Montant total", "Reste à payer", "Statut"]
    questions = [
        {
            "type": "text",
            "name": "cost",
            "message": "Quel est le montant du contrat ?",
        },
        {
            "type": "text",
            "name": "balance",
            "message": "Combien reste à payer ?",
        },
        {
            "type": "select",
            "name": "statut",
            "message": "A quelle étape en est le contrat ?",
            "choices": [statu.name.capitalize() for statu in ContractStatu],
        },
    ]
