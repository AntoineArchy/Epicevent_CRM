from epic_event_CRM.base import roles
from epic_event_CRM.base.form import BaseForm


class CollaboratorCreationForm(BaseForm):
    fields_display = [
        "Nom",
        "Prénom",
        "Nom d'utilisateur (EpicEvent/Mysql)",
        "Mot de passe (provisoire)",
        "Département",
    ]
    questions = [
        {
            "type": "text",
            "name": "first_name",
            "message": "Quel est le nom du collaborateur ?",
        },
        {
            "type": "text",
            "name": "last_name",
            "message": "Quel est le prénom du collaborateur ?",
        },
        {
            "type": "text",
            "name": "username",
            "message": "Quel nom d'utilisateur servira à la connexion du collaborateur ?",
        },
        {
            "type": "password",
            "name": "password",
            "message": "Indiquez le mot de passe provisoire du collaborateur (sera modifié lors de la première "
            "connexion de celui-ci)",
        },
        {
            "type": "select",
            "name": "department",
            "message": "A quel département sera rattaché le collaborateur ?",
            "choices": [dept.name.capitalize() for dept in roles.EpicEventRole],
        },
    ]
