from unittest.mock import MagicMock

from epic_event_CRM.base import controller
from epic_event_CRM.base import view
from epic_event_CRM.base.model import BaseModel


from epic_event_CRM.base.view import CreateView


def test_handle_user_input_base_view():
    context = MagicMock()
    context.last_user_input = "Any input"
    context.current_view = None
    chosen_view = view.BaseView

    controller.BaseController.handle_user_input(context, chosen_view)
    assert context.set_in_context.called_with(controller.BaseController.table)
    print(context, context.current_view)
    # assert context.current_view is chosen_view


def test_set_to_display():
    context = MagicMock()
    context.data_to_display = {
        "fields": ["old field"],
        "data": [["old_data"]],
    }

    controller.BaseController.set_to_display(context, fields=["new_field"])
    assert context.data_to_display == {"fields": ["new_field"], "data": [["old_data"]]}

    controller.BaseController.set_to_display(context, data=[["new_value"]])
    assert context.data_to_display == {"fields": ["new_field"], "data": [["new_value"]]}


def test_get_context_related_view():
    context = MagicMock()

    view1 = MagicMock()
    view1.can_display.return_value = True
    view1.has_requirements.return_value = True

    view2 = MagicMock()
    view2.can_display.return_value = False
    view2.has_requirements.return_value = True

    view3 = MagicMock()
    view3.can_display.return_value = True
    view3.has_requirements.return_value = False

    controller.BaseController.views = [view1, view2, view3]

    result = controller.BaseController.get_context_related_view(context)

    assert result == [(f"{view1.name_display}", view1, controller.BaseController)]


def test_get_allowed_views():
    # Crée un contexte simulé avec des vues simulées
    defined_context = dict()
    context = MagicMock()
    context.get_in_context.side_effect = lambda x: defined_context.get(x, None)

    # Définis des propriétés cohérentes pour les vues simulées
    view1 = MagicMock()
    view1.name_display = "View1"
    view1.can_display.return_value = True
    view1.allow_select = True

    view2 = MagicMock()
    view2.name_display = "View2"
    view2.can_display.return_value = (
        False  # Cette vue ne doit pas être incluse car can_display est False
    )
    view2.allow_select = True

    view3 = MagicMock()
    view3.name_display = "View3"
    view3.can_display.return_value = True
    view3.allow_select = True

    # Définis les vues de la classe BusinessLogic
    controller.BaseController.table = "table_test"
    controller.BaseController.views = [view1, view2, view3]

    # Définis une vue actuelle dans le contexte simulé
    context.current_view = None

    # Appelle la fonction get_allowed_views
    result = controller.BaseController.get_allowed_views(context)

    # Vérifie que la liste retournée correspond à ce à quoi tu t'attends
    expected_result = [
        (f"{view1.name_display}", view1, controller.BaseController),
        (f"{view3.name_display}", view3, controller.BaseController),
    ]
    assert result == expected_result
    context.current_view = "View of other controller"
    result = controller.BaseController.get_allowed_views(context)
    assert result == expected_result

    context.current_view = view1
    result = controller.BaseController.get_allowed_views(context)
    expected_result = [
        (f"Selection", view1, controller.BaseController),
        (f"{view3.name_display}", view3, controller.BaseController),
    ]
    assert result == expected_result

    defined_context[controller.BaseController.table] = True
    result = controller.BaseController.get_allowed_views(context)
    expected_result = [
        (f"Mettre à jour", view1, controller.BaseController),
        (f"{view3.name_display}", view3, controller.BaseController),
    ]
    assert result == expected_result


def test_return_view_selection_back():
    # Crée un contexte simulé avec des données cohérentes
    context = MagicMock()
    context.display.select_from_current_view.return_value = "back"

    # Simule une vue choisie
    chosen_view = MagicMock()

    # Appelle la fonction return_view_selection
    result = controller.BaseController.return_view_selection(context, chosen_view)
    expected_result = None
    assert result == expected_result


def test_return_view_selection_none():
    # Crée un contexte simulé avec des données cohérentes
    context = MagicMock()
    context.display.select_from_current_view.return_value = None
    # Simule une vue choisie
    chosen_view = MagicMock()

    # Appelle la fonction return_view_selection
    result = controller.BaseController.return_view_selection(context, chosen_view)
    expected_result = None
    assert result == expected_result


def test_return_view_selection_index_0():
    # Crée un contexte simulé avec des données cohérentes
    context = MagicMock()
    context.display.select_from_current_view.return_value = "0"
    context.data_to_display = {
        "fields": ["Field1", "Field2"],
        "data": [["Value1", "Value2"], ["Value3", "Value4"]],
    }

    # Simule une vue choisie
    chosen_view = view.BaseView

    # Appelle la fonction return_view_selection
    result = controller.BaseController.return_view_selection(context, chosen_view)
    expected_result = BaseModel(Field1="Value1", Field2="Value2")
    assert result == expected_result


# def test_return_view_selection():
#     # Crée un contexte simulé avec des données cohérentes
#     context = MagicMock()
#     context.display.select_from_current_view.return_value = (
#         "back"  # Simule la sélection de l'index 1
#     )
#     context.data_to_display = {
#         "fields": ["Field1", "Field2"],
#         "data": [["Value1", "Value2"], ["Value1", "Value2"]],
#     }
#
#     serializer = MagicMock()
#     controller.BaseController.serializers = serializer
#
#     # Simule une vue choisie
#     chosen_view = MagicMock()
#     chosen_view.view_name = "TestView"
#     chosen_view.name_display = "Test View"
#
#     # Appelle la fonction return_view_selection
#     result = controller.BaseController.return_view_selection(context, chosen_view)
#     expected_result = None
#     assert result == expected_result
#
#     context.display.select_from_current_view.return_value = (
#         "back"  # Simule la sélection de l'index 1
#     )
#     result = controller.BaseController.return_view_selection(context, chosen_view)
#     expected_result = None
#     assert result == expected_result
#
#     context.display.select_from_current_view.return_value = (
#         "0"  # Simule la sélection de l'index 1
#     )
#     serializer.create_obj_from_view.return_value = "0"
#
#     result = controller.BaseController.return_view_selection(context, chosen_view)
#     expected_result = "0"
#     assert result == expected_result


def test_handle_user_input_selection():
    context = MagicMock()
    context.data_to_display = dict()
    chosen_view = view.BaseView
    selected_obj = MagicMock()

    controller.BaseController.return_view_selection = MagicMock(
        return_value=selected_obj
    )
    context.last_user_input = "selection"

    controller.BaseController.handle_user_input(context, chosen_view)

    assert context.display.clear.called
    assert controller.BaseController.return_view_selection.called_with(
        context, chosen_view
    )
    assert context.set_in_context.called_with(
        controller.BaseController.table, selected_obj
    )
    assert context.clear.called_once()


def test_handle_user_input_selection_is_none():
    context = MagicMock()
    context.data_to_display = dict()
    chosen_view = view.BaseView

    controller.BaseController.return_view_selection = MagicMock(return_value=None)
    context.last_user_input = "selection"

    controller.BaseController.handle_user_input(context, chosen_view)

    assert context.display.clear.called
    assert context.clear.called_once()


def test_handle_user_input_mise_a_jour():
    context = MagicMock()
    context.data_to_display = dict()
    chosen_view = view.BaseView
    context.last_user_input = "mettre à jour"

    controller.BaseController.update = MagicMock()
    controller.BaseController.handle_user_input(context, chosen_view)

    assert controller.BaseController.update.called_with(
        controller.BaseController, context
    )


def test_handle_user_input_create_view():
    context = MagicMock()
    context.data_to_display = dict()
    chosen_view = CreateView
    context.last_user_input = "Any input on create view"

    controller.BaseController.create = lambda _: view.BaseView
    controller.BaseController.save = lambda _, v: _

    controller.BaseController.handle_user_input(context, chosen_view)

    # assert context.data_to_display["fields"] == view.BaseView.__dict__.keys()
    # list_view_values = list(view.BaseView.__dict__.values())
    # list_data_values = list(context.data_to_display["data"])
    # assert list_data_values == list_view_values
    # assert context.current_view == chosen_view
    assert context.set_in_context.called_once_with(
        controller.BaseController.table, MagicMock()
    )
    assert context.clear.called_once()
