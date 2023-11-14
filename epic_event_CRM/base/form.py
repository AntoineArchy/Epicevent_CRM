from __future__ import annotations

from typing import List, Dict


class BaseForm:
    fields_display = None
    questions = None
    formats = None

    @classmethod
    def get_fields(cls):
        return cls.fields_display

    @classmethod
    def get_from_field_form(cls, to_include_fields: List) -> List | None:
        selected_fields = list()
        for question in cls.questions:
            if question.get("name") in to_include_fields:
                selected_fields.append(question)
        if not selected_fields:
            return None
        return selected_fields

    @classmethod
    def update_obj_form(cls, obj_form: Dict, fields_to_update: Dict) -> Dict:
        allowed_update_fields = [question.get("name") for question in cls.questions]
        for field_name, valu in fields_to_update.items():
            if field_name not in allowed_update_fields:
                continue
            obj_form[field_name] = valu
        return obj_form
