from unittest import mock

from base import authorization
from base.view import BaseView, CreateView, set_table_allias, get_filters
from epic_event_CRM.collaborator.model import Collaborator


class BaseViewWithAuthorization(BaseView):
    view_authorization = [authorization.IsGestion]


class BaseViewWithContextRequirements(BaseView):
    context_requirements = ["requirement1", "requirement2"]


class BaseViewComplete(BaseView):
    view_name = "my_table"
    fields_name = ["field1", "field2"]
    fields_name_display = ["alias1", "alias2"]
    filter = "field1 = 'value'"
    default_order = "field2 ASC"
    context_requirements = ["requirement1", "requirement2"]
    optional_context_requirements = ["optional_requirement"]
    view_authorization = [authorization.IsGestion]


def test_set_table_allias():
    fields = ["field1", "field2"]
    field_display = ["alias1", "alias2"]
    result = set_table_allias(fields, field_display)
    assert result == "field1 AS 'alias1', field2 AS 'alias2'"


def test_set_table_allias_with_none_fields():
    result = set_table_allias(None, ["Random"])
    assert result == "*"


def test_set_table_allias_with_none_allias():
    result = set_table_allias(["Random"], None)
    assert result == "Random AS 'Random'"


def test_get_filters_with_filter():
    result = get_filters("field1 = 'value'")
    assert result == "WHERE field1 = 'value'"


def test_get_filters_without_filter():
    result = get_filters(None)
    assert result == ""


def test_create_view_inherits_from_base_view():
    assert issubclass(CreateView, BaseView)


class TestBaseView:
    def test_is_basic_collaborator_user_authorize_to_view_basic_view(self):
        collaborator = Collaborator()
        view = BaseView()

        assert view.is_user_authorize_to_view(collaborator)

    def test_is_basic_collaborator_user_authorize_to_view_authorized_view(self):
        collaborator = Collaborator()
        view = BaseViewWithAuthorization()

        assert not view.is_user_authorize_to_view(collaborator)

    def test_has_requirements_without_requirements(self):
        view = BaseView()
        assert not view.has_requirements()

    def test_has_requirements_with_requirements(self):
        view = BaseViewWithContextRequirements()
        assert view.has_requirements()

    def test_are_requirements_meet_without_requirements(self):
        view = BaseView()
        assert view.are_requirements_meet(None)

    @mock.patch("base.context.Context", autospec=True)
    def test_are_requirements_meet_with_requirements_met(self, mock_context_cls):
        defined_context = {"requirement1": True, "requirement2": True}
        mock_context_instance = mock_context_cls.return_value
        mock_context_instance.get_in_context.side_effect = (
            lambda x: defined_context.get(x, None)
        )

        view = BaseViewWithContextRequirements()
        assert view.are_requirements_meet(mock_context_instance)

    @mock.patch("base.context.Context", autospec=True)
    def test_can_display_without_authorization(self, mock_context_cls):
        view = BaseView()
        collaborator_instance = Collaborator()
        mock_context_instance = mock_context_cls.return_value
        mock_context_instance.current_user = collaborator_instance

        assert view.can_display(mock_context_instance)

    @mock.patch("base.context.Context", autospec=True)
    def test_can_display_with_authorization(self, mock_context_cls):
        view = BaseViewWithAuthorization()
        collaborator_instance = Collaborator()
        mock_context_instance = mock_context_cls.return_value
        mock_context_instance.current_user = collaborator_instance

        assert not view.can_display(mock_context_instance)

    @mock.patch("base.context.Context", autospec=True)
    def test_can_display_with_requirements_met(self, mock_context_cls):
        view = BaseViewWithContextRequirements()
        collaborator_instance = Collaborator()

        mock_context_instance = mock_context_cls.return_value
        mock_context_instance.current_user = collaborator_instance
        defined_context = {
            "requirement1": True,
            "requirement2": True,
        }

        mock_context_instance = mock_context_cls.return_value
        mock_context_instance.get_in_context.side_effect = (
            lambda x: defined_context.get(x, None)
        )
        assert view.can_display(mock_context_instance)

    def test_get_query_with_filter(self):
        view = BaseViewComplete()
        expected_query = "SELECT field1 AS 'alias1', field2 AS 'alias2' FROM my_table WHERE field1 = 'value';"

        assert view.get_query()[0].replace(" ", "").replace(
            "\n", ""
        ) == expected_query.replace(" ", "").replace("\n", "")
