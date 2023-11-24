from unittest.mock import MagicMock
import pytest

from base.context import Context


@pytest.fixture
def mock_context():
    connector = MagicMock()
    display = MagicMock()
    return Context(connector, display)


def test_clear_context(mock_context):
    mock_context.current_view = "TestView"
    mock_context.data_to_display = {
        "fields": ["Field1", "Field2"],
        "data": [["Value1", "Value2"]],
    }
    mock_context.last_user_input = "input"
    mock_context.current_available_option = [("Option1", None, None)]
    mock_context.in_context = {"key": "value"}

    mock_context.clear()

    assert mock_context.current_view is None
    assert mock_context.data_to_display == {"fields": None, "data": None}
    assert mock_context.last_user_input is None
    assert mock_context.current_available_option is None
    assert mock_context.in_context == {}


def test_set_in_context(mock_context):
    mock_context.set_in_context("key", "value")

    assert mock_context.in_context == {"key": "value"}
    assert mock_context.get_in_context("key") == "value"


def test_get_in_context_existing_key(mock_context):
    mock_context.set_in_context("key", "value")

    result = mock_context.get_in_context("key")

    assert result == "value"


def test_get_in_context_nonexistent_key(mock_context):
    result = mock_context.get_in_context("nonexistent_key")

    assert result is None


def test_get_user_choice_matching_input(mock_context):
    mock_context.current_available_option = [
        ("Option1", "value1", "action1"),
        ("Option2", "value2", "action2"),
    ]

    mock_context.last_user_input = "Option1"

    result = mock_context.get_user_choice()

    assert result == ("Option1", "value1", "action1")


def test_get_user_choice_nonmatching_input(mock_context):
    mock_context.current_available_option = [
        ("Option1", "value1", "action1"),
        ("Option2", "value2", "action2"),
    ]

    mock_context.last_user_input = "NonMatchingOption"

    result = mock_context.get_user_choice()

    assert result == (None, None)


def test_get_dynamic_menu_with_view(mock_context):
    mock_context.current_available_option = [
        ("Option1", "value1", "action1"),
        ("Option2", "value2", "action2"),
    ]

    mock_context.current_view = "TestView"

    result = mock_context.get_dynamic_menu()

    assert result == ["Option1", "Option2", "Menu principal"]


def test_get_dynamic_menu_without_view(mock_context):
    mock_context.current_available_option = [
        ("Option1", "value1", "action1"),
        ("Option2", "value2", "action2"),
    ]

    result = mock_context.get_dynamic_menu()

    assert result == ["Option1", "Option2"]
    assert "Menu principal" not in result


def test_get_data_length_zero(mock_context):
    assert mock_context.get_data_length() == 0


def test_get_data_length_non_zero(mock_context):
    mock_context.set_current_display(data=["data1", "data2"])
    assert mock_context.get_data_length() != 0


def test_set_current_display_view(mock_context):
    mock_context.set_current_display(view="TestView")
    assert mock_context.current_view == "TestView"


def test_set_current_display_fields(mock_context):
    mock_context.set_current_display(fields=["field1", "fields2"])
    assert mock_context.data_to_display["fields"] == ["field1", "fields2"]


def test_set_current_display_data(mock_context):
    mock_context.set_current_display(data=["data1", "data1"])
    assert mock_context.data_to_display["data"] == ["data1", "data1"]
