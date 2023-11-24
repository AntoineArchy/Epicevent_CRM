from unittest.mock import MagicMock

from epic_event_CRM.event.form import EventCreationForm


def test_get_fields_with_gestion_role():
    # Teste la fonction get_fields lorsque l'utilisateur a le rôle EpicEventRole.gestion
    mock_context = MagicMock()
    mock_context.current_user.has_role.return_value = True

    result = EventCreationForm.get_fields(mock_context)

    assert result == ["Modifier le collaborateur support"]


def test_get_fields_without_gestion_role():
    # Teste la fonction get_fields lorsque l'utilisateur n'a pas le rôle EpicEventRole.gestion
    mock_context = MagicMock()
    mock_context.current_user.has_role.return_value = False

    result = EventCreationForm.get_fields(mock_context)

    assert result == EventCreationForm.fields_display


def test_get_question_with_custom_field():
    # Teste la fonction get_question pour un champ personnalisé
    field = "Modifier le collaborateur support"
    result = EventCreationForm.get_question(field)

    assert result == "Select_Collaborator"


def test_get_question_with_default_field():
    # Teste la fonction get_question pour un champ par défaut
    field = "Nom"
    result = EventCreationForm.get_question(field)

    assert result == {
        "type": "text",
        "name": "name",
        "message": "Quel est le nom de l'événement ?",
    }
