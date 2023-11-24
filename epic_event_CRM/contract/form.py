from enum import Enum

from base.form import BaseForm


class ContractStatus(Enum):
    to_sign = "À signer"
    signed = "Signé"
    to_pay = "Reste à payer"
    payed = "Payé"


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
            "choices": [statu.value.capitalize() for statu in ContractStatus],
        },
    ]
