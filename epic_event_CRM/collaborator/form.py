from base import roles
from base.form import BaseForm


class CollaboratorCreationForm(BaseForm):
    fields_display = [
        "Nom",
        "Prénom",
        "Nom d'utilisateur (EpicEvent/Mysql)",
        "Mot de passe",
        "Département",
    ]
    questions = [
        {
            "type": "text",
            "name": "last_name",
            "message": "Quel est le nom du collaborateur ?",
        },
        {
            "type": "text",
            "name": "first_name",
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
            "message": "Indiquez le mot de passe du collaborateur",
        },
        {
            "type": "select",
            "name": "department",
            "message": "A quel département sera rattaché le collaborateur ?",
            "choices": [dept.name.capitalize() for dept in roles.EpicEventRole],
        },
    ]
