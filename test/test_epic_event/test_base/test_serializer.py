from unittest.mock import MagicMock

from epic_event_CRM.base import authorization
from epic_event_CRM.base.model import BaseModel
from epic_event_CRM.base.serializer import BaseSerializer
from epic_event_CRM.collaborator.model import Collaborator
from epic_event_CRM.base.serializer import (
    construct_col_name_for_query,
    construct_val_name_for_query,
)


class BaseSerializerWithCreateAuth(BaseSerializer):
    create_authorization = [authorization.IsGestion, authorization.IsCollaborator]


class BaseSerializerWithUpdateAuth(BaseSerializer):
    update_authorization = [authorization.IsGestion, authorization.IsCollaborator]


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


def test_is_user_authorize_to_create_no_auth():
    serializer = BaseSerializer()
    user = Collaborator()
    assert not serializer.is_user_authorize_to_create(user)


def test_is_user_authorize_to_update_no_auth():
    serializer = BaseSerializer()
    user = Collaborator()
    assert not serializer.is_user_authorize_to_update(user)


def test_is_user_authorize_to_create_with_auth():
    serializer = BaseSerializerWithCreateAuth()
    user = Collaborator()
    assert serializer.is_user_authorize_to_create(user)


def test_is_user_authorize_to_update_with_auth():
    serializer = BaseSerializerWithUpdateAuth()
    user = Collaborator()
    assert serializer.is_user_authorize_to_update(user)


def test_create_obj_from_view():
    serializer = BaseSerializer()

    view_data = {"Field1": "value1", "Field2": "value2"}
    obj = serializer.create_obj_from_view(view_data)

    assert obj == view_data


def test_is_user_authorize_to_update():
    serializer = BaseSerializer()
    serializer.update_authorization = [
        MagicMock(has_authorization=MagicMock(return_value=True))
    ]

    user = Collaborator()
    assert not serializer.is_user_authorize_to_update(user)


def test_create_obj_from_form():
    form_data = {"Field1": "value1", "Field2": "value2"}
    result = BaseSerializer.create_obj_from_form(form_data)

    expected_result = form_data
    assert result == expected_result


def test_get_blank_form():
    assert BaseSerializer.get_blank_form() == vars(BaseModel())
