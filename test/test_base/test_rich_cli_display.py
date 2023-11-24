from unittest.mock import patch, MagicMock
import os

from rich.table import Table

from base.display.rich_cli_display import (
    feed_table,
    get_table,
    display_query_results,
    RichQuestionaryCliDisplay,
)


def test_feed_table():
    # Crée un tableau de résultats simulé
    view_name = "TestView"
    results = {"fields": ["Field1", "Field2"], "data": [["Value1"], ["Value2"]]}

    table = Table(title=view_name)

    # Appelle la fonction feed_table
    table = feed_table(table, results, as_select=False)
    # Vérifie que le tableau a été construit correctement
    assert len(table.rows) == 2  # 1 row of fields + 1 row of data


def test_feed_table_select():
    # Crée un tableau de résultats simulé
    view_name = "TestView"
    results = {"fields": ["Field1", "Field2"], "data": [["Value1"], ["Value2"]]}
    table = Table(view_name)
    # Appelle la fonction feed_table
    table = feed_table(table, results, as_select=True)
    # Vérifie que le tableau a été construit correctement
    assert len(table.columns) == 2  # 2 fields + Selection Idx.
    assert len(table.rows) == 2  # 1 row of fields + 1 row of data
    # assert "Selection Idx." in table.columns[0]
    # assert "0" in table.columns
    # assert "Value1" in table.rows[1]
    # assert "Value2" in table.rows[1]


def test_get_table():
    # Crée des résultats simulés
    view_name = "TestView"
    results = {"fields": ["Field1", "Field2"], "data": [["Value1"], ["Value2"]]}

    # Appelle la fonction get_table
    table = get_table(view_name, results, as_select=True)

    # Vérifie que le tableau a été correctement obtenu
    assert len(table.columns) == 3
    assert len(table.rows) == 2


def test_display_query_results(capsys):
    # Crée des résultats simulés
    view_name = "TestView"
    results = {"fields": ["Field1", "Field2"], "data": [["Value1", "Value2"]]}

    # Appelle la fonction display_query_results
    display_query_results(view_name, results, as_select=True)
    # Capture la sortie standard et vérifie qu'elle contient les résultats
    captured = capsys.readouterr()
    assert "TestView" in captured.out
    assert "Field1" in captured.out
    assert "Value1" in captured.out

    RichQuestionaryCliDisplay.display_actual_view(view_name, results)
    captured = capsys.readouterr()
    assert "TestView" in captured.out
    assert "Field1" in captured.out
    assert "Value1" in captured.out


def test_clear(monkeypatch):
    # Utilise monkeypatch pour remplacer os.system et tester l'appel à clear()
    with patch("os.system") as mocked_os_system:
        RichQuestionaryCliDisplay.clear()
        mocked_os_system.assert_called_once_with("cls" if os.name == "nt" else "clear")


def test_select_from_current_view(monkeypatch):
    # Crée des résultats simulés
    view_name = "TestView"
    data_to_display = {"fields": ["Field1", "Field2"], "data": [["Value1", "Value2"]]}

    # Utilise monkeypatch pour fournir une réponse simulée à la sélection
    with patch("questionary.select") as mocked_questionary_select:
        mocked_questionary_select.return_value.ask.return_value = "0"

        # Appelle la fonction select_from_current_view
        selected_idx = RichQuestionaryCliDisplay.select_from_current_view(
            view_name, data_to_display
        )

        # Vérifie que la fonction select a été appelée avec les bons arguments
        mocked_questionary_select.assert_called_once_with(
            "Selection n° : ",
            choices=["0", "Back"],
        )

        # Vérifie que la valeur sélectionnée est correcte
        assert selected_idx == "0"


def test_update():
    # Crée un contexte simulé avec une vue actuelle et des données à afficher
    context = MagicMock()
    context.current_view = MagicMock()
    context.current_view.name_display = "TestView"
    context.data_to_display = {
        "fields": ["Field1", "Field2"],
        "data": [["Value1", "Value2"]],
    }

    # Crée un simulateur de console riche pour les tests
    display = RichQuestionaryCliDisplay()

    # Mocke la méthode display_actual_view pour vérifier si elle est appelée
    with patch.object(
        display, "display_actual_view", return_value=None
    ) as mock_display_actual_view:
        # Mocke la méthode get_user_input pour retourner une valeur simulée
        with patch.object(
            display, "get_user_input", return_value="user_input"
        ) as mock_get_user_input:
            # Appelle la méthode update
            display.update(context)

    # Vérifie que la méthode display_actual_view a été appelée avec les bons arguments
    mock_display_actual_view.assert_called_once_with(
        "TestView", {"fields": ["Field1", "Field2"], "data": [["Value1", "Value2"]]}
    )

    # Vérifie que la méthode get_user_input a été appelée avec le contexte
    mock_get_user_input.assert_called_once_with(context)

    # Vérifie que le dernier user input dans le contexte a été mis à jour
    assert context.last_user_input == "user_input"
