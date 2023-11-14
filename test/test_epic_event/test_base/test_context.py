from unittest.mock import MagicMock

from epic_event_CRM.base.context import Context


def test_clear_context():
    connector = MagicMock()
    display = MagicMock()
    context = Context(connector, display)

    # Simule l'état initial du contexte
    context.current_view = "TestView"
    context.data_to_display = {
        "fields": ["Field1", "Field2"],
        "data": [["Value1", "Value2"]],
    }
    context.last_user_input = "input"
    context.current_available_option = [("Option1", None, None)]
    context.in_context = {"key": "value"}

    # Appelle la méthode clear
    context.clear()

    # Vérifie que tous les attributs ont été réinitialisés
    assert context.current_view is None
    assert context.data_to_display == {"fields": None, "data": None}
    assert context.last_user_input is None
    assert context.current_available_option is None
    assert context.in_context == {}


def test_set_in_context():
    connector = MagicMock()
    display = MagicMock()
    context = Context(connector, display)

    # Simule l'ajout d'un objet dans le contexte
    context.set_in_context("key", "value")

    # Vérifie que l'objet a bien été ajouté au contexte
    assert context.in_context == {"key": "value"}


def test_get_in_context_existing_key():
    connector = MagicMock()
    display = MagicMock()
    context = Context(connector, display)

    # Simule l'ajout d'un objet dans le contexte
    context.set_in_context("key", "value")

    # Appelle la méthode get_in_context pour un key existant
    result = context.get_in_context("key")

    # Vérifie que l'objet a bien été récupéré du contexte
    assert result == "value"


def test_get_in_context_nonexistent_key():
    connector = MagicMock()
    display = MagicMock()
    context = Context(connector, display)

    # Appelle la méthode get_in_context pour un key inexistant
    result = context.get_in_context("nonexistent_key")

    # Vérifie que None est retourné car le key n'existe pas dans le contexte
    assert result is None


def test_get_user_choice_matching_input():
    connector = MagicMock()
    display = MagicMock()
    context = Context(connector, display)

    # Définit la liste des options disponibles
    context.current_available_option = [
        ("Option1", "value1", "action1"),
        ("Option2", "value2", "action2"),
    ]

    # Simule la saisie de l'utilisateur
    context.last_user_input = "Option1"

    # Appelle la méthode get_user_choice
    result = context.get_user_choice()

    # Vérifie que l'option correspondant à la saisie de l'utilisateur est retournée
    assert result == ("Option1", "value1", "action1")


def test_get_user_choice_nonmatching_input():
    connector = MagicMock()
    display = MagicMock()
    context = Context(connector, display)

    # Définit la liste des options disponibles
    context.current_available_option = [
        ("Option1", "value1", "action1"),
        ("Option2", "value2", "action2"),
    ]

    # Simule une saisie de l'utilisateur qui ne correspond à aucune option
    context.last_user_input = "NonMatchingOption"

    # Appelle la méthode get_user_choice
    result = context.get_user_choice()

    # Vérifie que None est retourné car la saisie de l'utilisateur ne correspond à aucune option
    assert result == (None, None)


def test_get_dynamic_menu_with_view():
    connector = MagicMock()
    display = MagicMock()
    context = Context(connector, display)

    # Définit la liste des options disponibles
    context.current_available_option = [
        ("Option1", "value1", "action1"),
        ("Option2", "value2", "action2"),
    ]

    # Définit une vue actuelle
    context.current_view = "TestView"

    # Appelle la méthode get_dynamic_menu
    result = context.get_dynamic_menu()

    # Vérifie que l'option "Menu principal" est ajoutée à la liste des options
    assert result == ["Option1", "Option2", "Menu principal"]


def test_get_dynamic_menu_without_view():
    connector = MagicMock()
    display = MagicMock()
    context = Context(connector, display)

    # Définit la liste des options disponibles
    context.current_available_option = [
        ("Option1", "value1", "action1"),
        ("Option2", "value2", "action2"),
    ]

    # Appelle la méthode get_dynamic_menu sans vue actuelle
    result = context.get_dynamic_menu()

    # Vérifie que la liste des options est inchangée car il n'y a pas de vue actuelle
    assert result == ["Option1", "Option2"]
    assert "Menu principal" not in result
