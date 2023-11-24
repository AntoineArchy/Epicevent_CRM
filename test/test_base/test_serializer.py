from base.serializer import (
    construct_col_name_for_query,
    construct_val_name_for_query,
)


def test_construct_col_name_for_query():
    obj_data = {"field1": "value1", "field2": "value2"}
    result = construct_col_name_for_query(obj_data)
    expected_result = "(field1, field2)"
    assert result == expected_result


def test_construct_val_name_for_query():
    obj_data = {"field1": "value1", "field2": "value2"}
    result = construct_val_name_for_query(obj_data)
    expected_result = ("value1", "value2")
    assert result == expected_result
