from typing import Dict, Tuple, Callable

import questionary

from SQL.connector import Connector
from epic_event_CRM.base.model import BaseModel
from epic_event_CRM.collaborator.model import Collaborator


def construct_col_name_for_query(obj_data: Dict) -> str:
    return f"{tuple([*obj_data.keys()])}".replace("'", "")


def construct_val_name_for_query(obj_data: Dict) -> Tuple:
    return tuple([*obj_data.values()])


class BaseSerializer:
    model = BaseModel
    table = None

    create_authorization = []
    update_authorization = []

    name_display = None

    @classmethod
    def is_user_authorize_to_create(cls, user: Collaborator) -> bool:
        for auth in cls.create_authorization:
            if auth.has_authorization(user):
                return True
        return False

    @classmethod
    def create_obj_from_view(cls, view_data: Dict) -> Dict:
        return view_data

    @classmethod
    def is_user_authorize_to_update(cls, user: Collaborator) -> bool:
        for auth in cls.update_authorization:
            if auth.has_authorization(user):
                return True
        return False

    @classmethod
    def create_obj_from_form(cls, form: Dict) -> Dict:
        return form

    @classmethod
    def get_blank_form(cls) -> Dict:
        return vars(cls.model())

    @classmethod
    def get_obj_dict(cls, obj: Callable) -> Dict:
        return obj.__dict__

    @classmethod
    def from_view_data_to_obj_dict(cls, view_data: Dict) -> Dict:
        return view_data

    @classmethod
    def from_obj_to_view_data(cls, obj: Callable) -> Dict:
        obj_dict = cls.get_obj_dict(obj)
        return cls.from_obj_dict_to_view_data(obj_dict)

    @classmethod
    def from_obj_dict_to_view_data(cls, obj_dict: Dict) -> Dict:
        return obj_dict

    @classmethod
    def from_obj_dict_to_form(cls, obj: Callable) -> None:
        return None

    @classmethod
    def from_form_to_obj_dict(cls, form: Dict) -> None:
        return None
