from __future__ import annotations

from typing import List, Dict

from SQL.connector import Connector
from epic_event_CRM.base.form import BaseForm
from epic_event_CRM.base.model import BaseModel
from epic_event_CRM.base.serializer import BaseSerializer
from epic_event_CRM.base.view import BaseView, CreateView
from epic_event_CRM.base.context import Context


class BaseController:
    views = [BaseView, CreateView]
    serializers = BaseSerializer

    table = None

    model = BaseModel
    form = BaseForm

    @classmethod
    def fill_obj_form(cls, context):
        filled_form = context.display.fill_form(cls.form)
        return filled_form

    @classmethod
    def create(cls, context: Context, form: Dict = None) -> BaseModel:
        if form is None:
            form = cls.fill_obj_form(context)
        created_obj = cls.model(**form)
        return created_obj

    @classmethod
    def update(
        cls,
        fields_to_update: Dict,
        context: Context,
        obj_to_update: BaseModel | None = None,
    ) -> None:
        if obj_to_update is None:
            obj_to_update = context.get_in_context(cls.table).get(cls.table)

        obj_form = cls.serializers.get_obj_dict(obj_to_update)
        updated_dict = cls.form.update_obj_form(obj_form, fields_to_update)
        updated_obj = cls.serializers.create_obj_from_form(updated_dict)
        cls.save(python_object=updated_obj, connector=context.current_connector)
        context.clear()

    @classmethod
    def set_to_display(
        cls, context: Context, fields: List = None, data: List = None
    ) -> None:
        if fields is not None:
            context.data_to_display["fields"] = fields

        if data is not None:
            context.data_to_display["data"] = data

    @classmethod
    def save(cls, python_object: BaseModel, connector: Connector) -> None:
        obj_data = python_object.__dict__
        obj_id = obj_data.pop(python_object.id_name)
        if obj_id == -1:
            connector.create(cls.table, obj_data)
            return
        connector.update(cls.table, obj_data)
        return

    @classmethod
    def get_context_related_view(cls, context: Context) -> List:
        allowed = list()

        for view in cls.views:
            if not view.can_display(context):
                continue

            if not view.has_requirements():
                continue
            allowed.append((f"{view.name_display}", view, cls))

        return allowed

    @classmethod
    def get_allowed_views(cls, context: Context) -> List:
        if context.current_view is not None and context.current_view not in cls.views:
            return cls.get_context_related_view(context)

        allowed = list()
        for view in cls.views:
            if not view.can_display(context):
                continue

            if context.current_view == view and view.allow_select:
                if context.get_in_context(cls.table) is not None:
                    allowed.append((f"Mettre à jour", view, cls))
                    continue
                allowed.append((f"Selection", view, cls))
                continue

            allowed.append((f"{view.name_display}", view, cls))
        return allowed

    @classmethod
    def return_view_selection(
        cls, context: Context, chosen_view: BaseView
    ) -> BaseModel:
        selected_idx = context.display.select_from_current_view(
            chosen_view.view_name, data_to_display=context.data_to_display
        )
        if selected_idx is None or selected_idx.lower() == "back":
            return None

        selected_in_list = dict(
            zip(
                context.data_to_display["fields"],
                context.data_to_display["data"][int(selected_idx)],
            )
        )
        # form = cls.serializers.create_obj_from_view(selected_in_list)
        form = cls.serializers.from_view_data_to_obj_dict(selected_in_list)
        selected_obj = cls.create(context, form=form)
        return selected_obj

    @classmethod
    def handle_user_select(cls, context, chosen_view):
        context.display.clear()
        selected_obj = cls.return_view_selection(context, chosen_view)
        if selected_obj is None:
            context.clear()
            return
        context.set_in_context(cls.table, selected_obj)
        obj_display = cls.serializers.from_obj_to_view_data(selected_obj)
        context.set_current_display(
            fields=obj_display.keys(), data=[obj_display.values()]
        )

    @classmethod
    def handle_user_update(cls, context):
        fields = context.display.select_field_from_form(cls.form)
        if fields is None:
            return

        updated_fields = context.display.fill_form(form_data=fields)
        cls.update(updated_fields, context)

    @classmethod
    def handle_user_create(cls, context, chosen_view):
        obj = cls.create(context)
        cls.save(obj, context.current_connector)
        context.set_current_display(
            view=chosen_view, fields=obj.__dict__.keys(), data=[obj.__dict__.values()]
        )
        context.set_in_context(cls.table, obj)

    @classmethod
    def handle_user_read(cls, context, chosen_view):
        results = context.current_connector.read(
            chosen_view.get_query(), include_fields=True
        )

        context.set_current_display(
            view=chosen_view, fields=results.pop(0), data=results
        )

    @classmethod
    def handle_user_input(cls, context: Context, chosen_view: BaseView) -> None:
        user_str_choice = context.last_user_input
        if user_str_choice.lower() == "selection":
            cls.handle_user_select(context, chosen_view)
            return

        elif user_str_choice.lower() == "mettre à jour":
            cls.handle_user_update(context)
            return

        elif issubclass(chosen_view, CreateView):
            cls.handle_user_create(context, chosen_view)
            return

        elif issubclass(chosen_view, BaseView):
            cls.handle_user_read(context, chosen_view)
            return
