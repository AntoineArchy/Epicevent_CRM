from __future__ import annotations

from curses.ascii import isdigit
from typing import List, Dict


class BaseForm:
    fields_display = None
    questions = None
    formats = None

    @classmethod
    def get_fields(cls, context):
        """
        Obtient la liste des champs du formulaire.

        Args:
            context: Objet contexte.

        Returns:
            List: Liste des champs du formulaire.
        """
        return list(cls.fields_display)

    @classmethod
    def get_question(cls, field):
        """
        Obtient la question associée à un champ spécifique.

        Args:
            field: Champ pour lequel obtenir la question.

        Returns:
            str: Question associée au champ.
        """
        field_idx = cls.fields_display.index(field)

        return cls.questions[field_idx]

    @classmethod
    def get_from_field_form(cls, to_include_fields: List) -> List | None:
        """
        Obtient les questions associées aux champs spécifiés.

        Args:
            to_include_fields (List): Liste des champs à inclure.

        Returns:
            List | None: Liste des questions associées ou None si aucun champ trouvé.
        """
        selected_fields = list()
        for question in cls.questions:
            if question.get("name") in to_include_fields:
                selected_fields.append(question)
        if not selected_fields:
            return None
        return selected_fields

    @classmethod
    def update_obj_form(cls, obj_form: Dict, fields_to_update: Dict) -> Dict:
        """
        Prépare un formulaire pour un objet avec les champs selectionné..

        Args:
            obj_form (Dict): Formulaire d'objet existant.
            fields_to_update (Dict): Champs à mettre à jour dans le formulaire.

        Returns:
            Dict: Formulaire des champs pret pour mise à jour.
        """
        allowed_update_fields = [question.get("name") for question in cls.questions]
        for field_name, valu in fields_to_update.items():
            if field_name not in allowed_update_fields:
                continue
            obj_form[field_name] = valu
        return obj_form
