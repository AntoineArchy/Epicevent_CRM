from base.form import BaseForm


class ClientCreationForm(BaseForm):
    fields_display = [
        "Nom du contact client",
        "Nom de l'entreprise du client",
        "Adresse mail liée au client",
        "Numéro lié au client",
    ]
    questions = [
        {
            "type": "text",
            "name": "full_name",
            "message": "Quel est le nom complet du contact chez le client ?",
        },
        {
            "type": "text",
            "name": "company_name",
            "message": "Quel est l'entreprise du client ?",
        },
        {
            "type": "text",
            "name": "email",
            "message": "Quelle est l'adresse mail du client ?",
        },
        {
            "type": "text",
            "name": "phone",
            "message": "Quel est le numéro du client ?",
        },
    ]
