from epic_event_CRM.base.form import BaseForm


def test_get_fields():
    class TestForm(BaseForm):
        fields_display = ["field1", "field2"]

    result = TestForm.get_fields()
    expected_result = ["field1", "field2"]
    assert result == expected_result


def test_get_from_field_form():
    class TestForm(BaseForm):
        fields_display = ["field1", "field2"]
        questions = [
            {"name": "field1", "text": "Field 1"},
            {"name": "field2", "text": "Field 2"},
            {"name": "field3", "text": "Field 3"},
        ]

    to_include_fields = ["field1", "field2"]

    result = TestForm.get_from_field_form(to_include_fields)
    expected_result = [
        {"name": "field1", "text": "Field 1"},
        {"name": "field2", "text": "Field 2"},
    ]
    assert result == expected_result


def test_update_obj_form():
    class TestForm(BaseForm):
        fields_display = ["field1", "field2"]
        questions = [
            {"name": "field1", "text": "Field 1"},
            {"name": "field2", "text": "Field 2"},
        ]

    obj_form = {"field1": "value1", "field2": "value2"}
    fields_to_update = {"field1": "new_value"}

    result = TestForm.update_obj_form(obj_form, fields_to_update)
    expected_result = {"field1": "new_value", "field2": "value2"}
    assert result == expected_result


def test_get_from_field_form_none():
    class TestForm(BaseForm):
        fields_display = ["field1", "field2"]
        questions = [
            {"name": "field1", "text": "Field 1"},
            {"name": "field2", "text": "Field 2"},
        ]

    to_include_fields = ["field3", "field4"]

    result = TestForm.get_from_field_form(to_include_fields)
    expected_result = None
    assert result == expected_result


def test_update_obj_form_invalid_fields():
    class TestForm(BaseForm):
        fields_display = ["field1", "field2"]
        questions = [
            {"name": "field1", "text": "Field 1"},
            {"name": "field2", "text": "Field 2"},
        ]

    obj_form = {"field1": "value1", "field2": "value2"}
    fields_to_update = {"field3": "value3", "field4": "value4"}

    result = TestForm.update_obj_form(obj_form, fields_to_update)
    expected_result = {"field1": "value1", "field2": "value2"}
    assert result == expected_result
