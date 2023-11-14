from __future__ import annotations

from typing import List

from epic_event_CRM.base import authorization
from epic_event_CRM.collaborator.model import Collaborator
from epic_event_CRM.base.context import Context


def set_table_allias(fields: List | None, field_display: List | None) -> str:
    if fields is None:
        return "*"

    if field_display is None:
        field_display = fields

    alias_str = ""
    for field, alias in zip(fields, field_display):
        alias_str += f"{field} AS '{alias}', "
    return alias_str[:-2]


def get_filters(view_filter: str | None) -> str:
    if view_filter is None:
        return ""
    return f"WHERE {view_filter}"


class BaseView:
    view_name = None
    name_display = None
    allow_select = False

    fields_name = None
    fields_name_display = None

    filter = None
    default_order = None

    context_requirements = None
    optional_context_requirements = None
    view_authorization = [authorization.IsCollaborator]

    @classmethod
    def is_user_authorize_to_view(cls, user: Collaborator) -> bool:
        for auth in cls.view_authorization:
            if not auth.has_authorization(user):
                return False
        return True

    @classmethod
    def has_requirements(cls) -> bool:
        return cls.context_requirements is not None

    @classmethod
    def are_requirements_meet(cls, context: Context) -> bool:
        if cls.context_requirements is None:
            return True
        for requirement in cls.context_requirements:
            if context.get_in_context(requirement) is None:
                return False
        return True

    @classmethod
    def can_display(cls, context: Context) -> bool:
        if not cls.is_user_authorize_to_view(context.current_user):
            return False
        if not cls.are_requirements_meet(context):
            return False
        return True

    @classmethod
    def get_query(cls) -> str:
        return f"""
        SELECT {set_table_allias(cls.fields_name, cls.fields_name_display)} 
        FROM {cls.view_name} 
        {get_filters(cls.filter) if cls.filter is not None else ''}; 
        """


class CreateView(BaseView):
    form = None
    model = None
