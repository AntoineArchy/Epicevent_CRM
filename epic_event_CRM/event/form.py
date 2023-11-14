from epic_event_CRM.base.form import BaseForm


class EventCreationForm(BaseForm):
    fields_display = ["Nom", "Début", "Fin", "Emplacement", "Participants", "Remarques"]
    questions = [
        {
            "type": "text",
            "name": "name",
            "message": "Quel est le nom de l'événement ?",
        },
        {
            "type": "text",
            "name": "event_start",
            "message": "Quel est la date et heure de début de l'événement ?",
        },
        {
            "type": "text",
            "name": "event_end",
            "message": "Quel est la date et heure de fin de l'événement ?",
        },
        {
            "type": "text",
            "name": "location",
            "message": "Ou aura lieu l'événement ?",
        },
        {
            "type": "text",
            "name": "attendees",
            "message": "Combien de personnes sont attendu à l'événement ?",
        },
        {
            "type": "text",
            "name": "notes",
            "message": "Ajoutez des remarque particulière.",
        },
    ]
